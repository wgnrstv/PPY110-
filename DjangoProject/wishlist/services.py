import json
import os
from django.contrib.auth import get_user


def view_in_wishlist(request, username: str) -> dict:
    """
    Функция для просмотра продуктов в избранном
    :param request: запрос от пользователя
    :param username: имя пользователя
    :return: Данные избранного в формате {username: {'products': [id1, id2, ...]}}
    """
    with open('wishlist.json', 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = {}

    if username in data:
        return data[username]
    return {}


def add_to_wishlist(request, id_product: str) -> bool:
    """
    Функция для добавления продукта в избранное
    :param request: запрос от пользователя
    :param id_product: ID продукта для добавления
    :return: Успех или неудача добавления продукта
    """
    current_user = get_user(request).username

    if current_user == "AnonymousUser":
        return False

    with open('wishlist.json', 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = {}

    if current_user not in data:
        data[current_user] = {'products': []}

    if id_product not in data[current_user]['products']:
        data[current_user]['products'].append(id_product)

        with open('wishlist.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)

        return True

    return False


def remove_from_wishlist(request, id_product: str) -> bool:
    """
    Функция для удаления продукта из избранного
    :param request: запрос от пользователя
    :param id_product: ID продукта для удаления
    :return: Успех или неудача удаления продукта
    """
    current_user = get_user(request).username

    if current_user == "AnonymousUser":
        return False

    with open('wishlist.json', 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = {}

    if current_user in data and id_product in data[current_user]['products']:
        data[current_user]['products'].remove(id_product)

        with open('wishlist.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)

        return True

    return False


def add_user_to_wishlist(request, username: str) -> bool:
    """
    Функция для добавления пользователя в базу данных избранного
    :param request: запрос от пользователя
    :param username: имя пользователя для добавления
    :return: Успех или неудача операции
    """
    if not os.path.exists('wishlist.json'):
        with open('wishlist.json', 'w', encoding='utf-8') as f:
            json.dump({}, f, ensure_ascii=False)

    with open('wishlist.json', 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = {}

    if username not in data:
        data[username] = {'products': []}

        with open('wishlist.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)

        return True

    return False