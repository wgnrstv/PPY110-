import json
import os
from typing import Dict, List, Union, Tuple
import hashlib


def save_data(data: Dict) -> None:
    """
    Сохраняет данные в JSON файл.

    Args:
        data (Dict): Словарь с данными пользователей.

    Returns:
        None
    """
    with open('users_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def load_data() -> Dict:
    """
    Загружает данные из JSON файла.

    Returns:
        Dict: Словарь с данными пользователей.
    """
    if os.path.exists('users_data.json'):
        try:
            with open('users_data.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("Ошибка при чтении файла данных. Создан новый файл.")
            return {}
    else:
        return {}


def hash_password(password: str) -> str:
    """
    Хеширует пароль пользователя.

    Args:
        password (str): Исходный пароль пользователя.

    Returns:
        str: Хешированный пароль.
    """

    return hashlib.sha256(password.encode()).hexdigest()


def authenticate() -> Tuple[str, Dict]:
    """
    Авторизация или регистрация пользователя.

    Returns:
        Tuple[str, Dict]: Кортеж, содержащий имя пользователя и словарь с данными пользователей.
    """
    data = load_data()

    while True:
        print("\n1. Авторизация")
        print("2. Регистрация")
        choice = input("Выберите действие (1/2): ")

        if choice == '1':
            username = input("Введите логин: ")
            password = input("Введите пароль: ")
            hashed_password = hash_password(password)

            if username in data and data[username]['password'] == hashed_password:
                print(f"\nДобро пожаловать, {username}!")
                return username, data
            else:
                print("Неверный логин или пароль.")

        elif choice == '2':
            username = input("Создайте новый логин: ")

            if username in data:
                print("Пользователь с таким именем уже существует.")
                continue

            password = input("Создайте пароль: ")
            hashed_password = hash_password(password)
            balance = validate_numeric_input("Введите начальный баланс: ")

            data[username] = {
                'password': hashed_password,
                'balance': balance,
                'expenses': [],
                'incomes': []
            }

            save_data(data)
            print(f"\nРегистрация завершена. Добро пожаловать, {username}!")
            return username, data

        else:
            print("Некорректный ввод. Пожалуйста, выберите 1 или 2.")


def validate_numeric_input(prompt: str) -> float:
    """
    Проверяет, что введенное значение является числом.

    Args:
        prompt (str): Приглашение для ввода.

    Returns:
        float: Проверенное числовое значение.
    """
    while True:
        try:
            value = float(input(prompt))
            return value
        except ValueError:
            print("Пожалуйста, введите числовое значение.")


def validate_index_input(prompt: str, max_index: int) -> int:
    """
    Проверяет, что введенный индекс находится в допустимом диапазоне.

    Args:
        prompt (str): Приглашение для ввода.
        max_index (int): Максимальный допустимый индекс.

    Returns:
        int: Проверенный индекс.
    """
    while True:
        try:
            index = int(input(prompt))
            if 1 <= index <= max_index:
                return index
            else:
                print(f"Пожалуйста, введите число от 1 до {max_index}.")
        except ValueError:
            print("Пожалуйста, введите целое число.")


def show_expenses_and_incomes(username: str, data: Dict) -> None:
    """
    Отображает расходы и доходы пользователя.

    Args:
        username (str): Имя пользователя.
        data (Dict): Словарь с данными пользователей.

    Returns:
        None
    """
    user_data = data[username]

    print("\n=== Ваши расходы ===")
    if user_data['expenses']:
        for i, expense in enumerate(user_data['expenses'], 1):
            print(f"{i}. {expense['description']}: {expense['amount']:.2f} руб.")
    else:
        print("У вас пока нет расходов.")

    print("\n=== Ваши доходы ===")
    if user_data['incomes']:
        for i, income in enumerate(user_data['incomes'], 1):
            print(f"{i}. {income['description']}: {income['amount']:.2f} руб.")
    else:
        print("У вас пока нет доходов.")

    print(f"\nТекущий баланс: {user_data['balance']:.2f} руб.")


def add_expense(username: str, data: Dict) -> None:
    """
    Добавляет новый расход.

    Args:
        username (str): Имя пользователя.
        data (Dict): Словарь с данными пользователей.

    Returns:
        None
    """
    description = input("Введите описание расхода: ")
    amount = validate_numeric_input("Введите сумму расхода: ")

    if amount <= 0:
        print("Сумма расхода должна быть положительной.")
        return

    if amount > data[username]['balance']:
        print("Недостаточно средств на балансе.")
        return

    data[username]['balance'] -= amount
    data[username]['expenses'].append({
        'description': description,
        'amount': amount
    })

    save_data(data)
    print(f"Расход добавлен. Новый баланс: {data[username]['balance']:.2f} руб.")


def add_income(username: str, data: Dict) -> None:
    """
    Добавляет новый доход.

    Args:
        username (str): Имя пользователя.
        data (Dict): Словарь с данными пользователей.

    Returns:
        None
    """
    description = input("Введите описание дохода: ")
    amount = validate_numeric_input("Введите сумму дохода: ")

    if amount <= 0:
        print("Сумма дохода должна быть положительной.")
        return

    data[username]['balance'] += amount
    data[username]['incomes'].append({
        'description': description,
        'amount': amount
    })

    save_data(data)
    print(f"Доход добавлен. Новый баланс: {data[username]['balance']:.2f} руб.")


def delete_expense(username: str, data: Dict) -> None:
    """
    Удаляет выбранный расход.

    Args:
        username (str): Имя пользователя.
        data (Dict): Словарь с данными пользователей.

    Returns:
        None
    """
    user_data = data[username]

    if not user_data['expenses']:
        print("У вас пока нет расходов для удаления.")
        return

    print("\n=== Ваши расходы ===")
    for i, expense in enumerate(user_data['expenses'], 1):
        print(f"{i}. {expense['description']}: {expense['amount']:.2f} руб.")

    index = validate_index_input(
        f"Выберите номер расхода для удаления (1-{len(user_data['expenses'])}): ",
        len(user_data['expenses'])
    )

    amount = user_data['expenses'][index - 1]['amount']
    user_data['balance'] += amount

    deleted_expense = user_data['expenses'].pop(index - 1)

    save_data(data)
    print(f"Расход '{deleted_expense['description']}' удален. Деньги возвращены на баланс.")
    print(f"Новый баланс: {user_data['balance']:.2f} руб.")


def delete_income(username: str, data: Dict) -> None:
    """
    Удаляет выбранный доход.

    Args:
        username (str): Имя пользователя.
        data (Dict): Словарь с данными пользователей.

    Returns:
        None
    """
    user_data = data[username]

    if not user_data['incomes']:
        print("У вас пока нет доходов для удаления.")
        return

    print("\n=== Ваши доходы ===")
    for i, income in enumerate(user_data['incomes'], 1):
        print(f"{i}. {income['description']}: {income['amount']:.2f} руб.")

    index = validate_index_input(
        f"Выберите номер дохода для удаления (1-{len(user_data['incomes'])}): ",
        len(user_data['incomes'])
    )

    amount = user_data['incomes'][index - 1]['amount']

    if amount > user_data['balance']:
        print("Недостаточно средств на балансе для удаления этого дохода.")
        return

    user_data['balance'] -= amount

    deleted_income = user_data['incomes'].pop(index - 1)

    save_data(data)
    print(f"Доход '{deleted_income['description']}' удален. Деньги сняты с баланса.")
    print(f"Новый баланс: {user_data['balance']:.2f} руб.")


def main() -> None:
    """
    Основная функция программы.

    Returns:
        None
    """
    print("*** Добро пожаловать в приложение учета расходов! ***")

    username, data = authenticate()

    while True:
        show_expenses_and_incomes(username, data)

        print("\nДоступные действия:")
        print("1. Добавить расход")
        print("2. Добавить доход")
        print("3. Удалить расход")
        print("4. Удалить доход")
        print("5. Выйти из программы")

        choice = input("\nВыберите действие (1-5): ")

        if choice == '1':
            add_expense(username, data)
        elif choice == '2':
            add_income(username, data)
        elif choice == '3':
            delete_expense(username, data)
        elif choice == '4':
            delete_income(username, data)
        elif choice == '5':
            print("Спасибо за использование приложения. До свидания!")
            break
        else:
            print("Некорректный ввод. Пожалуйста, выберите действие из списка.")


if __name__ == "__main__":
    main()