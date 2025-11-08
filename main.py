from src.menu_functions import choose_file, load_transactions, handle_cached_import, filter_dialog

def main():
    """main function"""
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

if __name__ == '__main__':
    main()