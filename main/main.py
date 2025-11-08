import traceback

from src.import_transactions import import_transactions_csv_excel_json
from src.menu_functions import exc_msg_dialog, load_cache, save_cache, \
    remove_empty_transactions, filter_by_state_dialog, sort_transactions_dialog, filter_currency_dialog, \
    filter_description_dialog, print_transactions, choose_file, load_transactions, handle_cached_import


def filter_dialog(transactions: list[dict]) -> None:
    print("\n")
    if not transactions:
        print("Файл не содержит транзакции.")
        return

    transactions = remove_empty_transactions(transactions)
    filtered_transactions = filter_by_state_dialog(transactions)
    if filtered_transactions is None or len(filtered_transactions) == 0:
        print("\nНе найдено ни одной транзакции с таким статусом.\n")
        return

    sort_transactions_dialog(filtered_transactions)
    currency_filtered_transactions = filter_currency_dialog(filtered_transactions)
    if len(currency_filtered_transactions) == 0:
        print("\nНе найдено ни одной транзакции в рублях.\n")
        return

    final_list = filter_description_dialog(currency_filtered_transactions)
    if len(final_list) == 0:
        print("\nНе найдено ни одной транзакции, подходящей под ваши условия фильтрации. \n")
        return

    print_transactions(final_list)


if __name__ == '__main__':
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    transactions: list[dict] | None = None

    while True:
        print("\nВыберите пункт меню:\n1. Получить информацию из файла\n2. Обработать предыдущий импорт\n3. Выход\n")
        choice = input().strip()

        if choice == '1':
            file_path = choose_file()
            if file_path:
                transactions = load_transactions(file_path)
                if transactions:
                    filter_dialog(transactions)

        elif choice == '2':
            transactions_cached = handle_cached_import()
            if transactions_cached:
                transactions = transactions_cached
                filter_dialog(transactions)

        elif choice == '3':
            print("\nЗавершение работы. До скорых встреч!")
            break

        else:
            print("\nТакого пункта меню нет. Попробуйте ещё раз.")
