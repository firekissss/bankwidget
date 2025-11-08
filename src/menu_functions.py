import json
import traceback

from src.config import CACHE_FILE
from src.external_api import convert_to_rub
from src.generators import filter_by_currency
from src.import_transactions import import_transactions_csv_excel_json
from src.processing import filter_by_state, sort_by_date, search_in_descriptions
from src.widget import get_date, mask_account_card


def save_cache(data: list[dict], source_filename: str):
    cache_data = {"source": source_filename, "transactions": data}
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache_data, f, ensure_ascii=False, indent=4)


def load_cache():
    if not CACHE_FILE.exists():
        return None
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def exc_msg_dialog(short, exc_info_stack):
    print("\n" + str(short))
    user_exc_info_detailed = input("Хотите узнать подробности ошибки? 1 - да, 0 - нет\t")
    if user_exc_info_detailed == '1':
        print(exc_info_stack + "\n")
        input("Нажмите Enter чтобы продолжить...")
    else:
        print()


def is_transaction_empty(transaction: dict) -> bool:
    def is_empty(value):
        if isinstance(value, dict):
            return all(is_empty(v) for v in value.values())
        return value in (None, "", [])

    return (not transaction) or all(is_empty(v) for v in transaction.values())


def formatted_transaction_output(transaction: dict) -> str:
    if not transaction:
        return "Пустая операция.\n"

    # --- дата ---
    try:
        date = get_date(transaction.get("date", ""))
    except ValueError:
        date = "Дата не указана или формат неверный."

    # --- описание ---
    description = transaction.get("description")
    description_str = description if description else "Описание отсутствует"

    # --- источники / получатели ---
    sender = transaction.get("from")
    receiver = transaction.get("to")

    if sender and receiver:
        trace = f"{mask_account_card(sender)} -> {mask_account_card(receiver)}"
    elif sender:
        trace = f"Снятие средств c: {mask_account_card(sender)}"
    elif receiver:
        trace = f"Перевод средств на: {mask_account_card(receiver)}"
    else:
        trace = "Нет данных о получателе и отправителе"

    # --- сумма ---
    amount_info = transaction.get("operationAmount") or {}
    amount = amount_info.get("amount")
    currency_name = (amount_info.get("currency") or {}).get("name", "")
    if amount:
        amount_str = f"{amount} {currency_name}".strip()
    else:
        amount_str = "отсутствует"

    output = (
        f"{date}\t{description_str}\n"
        f"{trace}\n"
        f"Сумма:\t{amount_str}\n"
    )

    return output


def remove_empty_transactions(transactions: list[dict]) -> list[dict]:
    empty_count = sum(1 for t in transactions if is_transaction_empty(t))
    if empty_count > 0:
        print(f"Пустые транзакции ({empty_count}), не содержащие никаких данных, будут удалены.\n")
    return [t for t in transactions if not is_transaction_empty(t)]


def filter_by_state_dialog(transactions: list[dict]) -> list[dict] | None:
    print("Введите статус, по которому необходимо выполнить фильтрацию.\n"
          "Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING\n"
          "Введите 0 для продолжения без фильтрации.")
    while True:
        state_to_filter = input("Статус: ").upper()
        try:
            if state_to_filter == "0":
                print()
                return transactions
            filtered = filter_by_state(transactions, state_to_filter)
            print(f"Операции успешно отфильтрованы по состоянию {state_to_filter}.\n")
            return filtered
        except ValueError as e:
            print(str(e))
        except Exception as e:
            exc_msg_dialog(e, traceback.format_exc())
            print("Пропустить фильтрацию по статусу? 1 - да, 0 - нет, выйти в главное меню")
            choice = input()
            if choice == "1":
                return transactions
            elif choice == "0":
                print("\n")
                continue
            else:
                return None


def sort_transactions_dialog(transactions: list[dict]) -> None:
    print("Сортировать по дате? 1 - да, 0 - нет")
    if input() == '1':
        print("Сортировка по убыванию. Изменить порядок? 1 - да, 0 - нет")
        sort_by_date(transactions, is_reversed=input() != '1')


def filter_currency_dialog(transactions: list[dict]) -> list[dict]:
    print("\nВыводить только рублевые транзакции? 1 - да, 0 - нет")
    if input() == '1':
        print("Перевести остальные транзакции в рубли? 1 - да, 0 - нет")
        if input() == '1':
            while True:
                try:
                    print("Осуществляется конвертация в рубли в соответствии с текущим курсом валют. Ожидайте...\n")
                    return [convert_to_rub(t) for t in transactions]
                except Exception as e:
                    exc_msg_dialog(e, traceback.format_exc())
                    print("1 - попробовать ещё раз, 0 - пропустить конвертацию")
                    if input() != '1':
                        print("Остальные транзакции не будут конвертированы в рубли.\n")
                        return transactions
        else:
            return list(filter_by_currency(transactions, "RUB"))
    return transactions


def filter_description_dialog(transactions: list[dict]) -> list[dict]:
    print("\nОтфильтровать список транзакций по определенному фрагменту в описании? 1 - да, 0 - нет")
    if input() == '1':
        search_pattern = input("Введите нужный фрагмент.\n"
                               "Транзакции, содержащие его в описании,\n"
                               "будут выведены на экран на следующем шаге: \t")
        return search_in_descriptions(transactions, search_pattern)
    print("Описание фильтроваться не будет.\n")
    return transactions


def print_transactions(transactions: list[dict]) -> None:
    if len(transactions) == 0:
        print("\nСписок транзакций пуст.\n")
        return
    print(f"Итоговый список транзакций (всего {len(transactions)}):\n")
    for transaction in transactions:
        try:
            print(formatted_transaction_output(transaction))
        except Exception as e:
            exc_msg_dialog(e, traceback.format_exc())


def choose_file() -> str | None:
    file_path = input("\nВведите путь к файлу или 0 для отмены:\n\n")
    if file_path == '0':
        return None
    return file_path


def load_transactions(file_path: str) -> list[dict] | None:
    try:
        transactions = import_transactions_csv_excel_json(file_path)
        save_cache(transactions, file_path)
        print("\nФайл успешно импортирован.")
        return transactions
    except Exception as e:
        exc_msg_dialog(e, traceback.format_exc())
        return None

def handle_cached_import() -> list[dict] | None:
    cache = load_cache()
    if not cache:
        print("\nВы ещё не импортировали ни одного файла.")
        return None

    filepath = cache["source"]
    choice = input(
        f"\nПредыдущий импорт был из файла {filepath}. "
        "1 - продолжить, 2 - обновить содержимое, 0 - отменить:\t"
    )

    if choice == '1':
        return cache['transactions']
    elif choice == '2':
        transactions = load_transactions(filepath)
        return transactions
    else:
        return None