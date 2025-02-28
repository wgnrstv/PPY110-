from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user
from .services import view_in_wishlist, add_to_wishlist, remove_from_wishlist

DATABASE = {}


@login_required(login_url='/login/')
def wishlist_view(request):
    """
    Представление для отображения страницы избранного
    """
    if request.method == "GET":
        current_user = get_user(request).username
        data = view_in_wishlist(request, current_user)

        products = []
        if data:
            product_ids = data['products']
            for product_id in product_ids:
                if product_id in DATABASE:
                    product = DATABASE[product_id]
                    products.append(product)

        return render(request, 'wishlist/wishlist.html', context={"products": products})


def wishlist_add_json(request, id_product: str):
    """
    Добавление продукта в избранное и возвращение информации об успехе или неудаче в JSON
    """
    if request.method == "GET":
        result = add_to_wishlist(request, id_product)
        if result:
            return JsonResponse({"answer": "Продукт успешно добавлен в избранное"},
                                json_dumps_params={'ensure_ascii': False})

        return JsonResponse({"answer": "Неудачное добавление в избранное"}, status=404,
                            json_dumps_params={'ensure_ascii': False})


def wishlist_del_json(request, id_product: str):
    """
    Удаление продукта из избранного и возвращение информации об успехе или неудаче в JSON
    """
    if request.method == "GET":
        result = remove_from_wishlist(request, id_product)
        if result:
            return JsonResponse({"answer": "Продукт успешно удалён из избранного"},
                                json_dumps_params={'ensure_ascii': False})

        return JsonResponse({"answer": "Неудачное удаление из избранного"}, status=404,
                            json_dumps_params={'ensure_ascii': False})


def wishlist_json(request):
    """
    Просмотр всех продуктов в избранном для пользователя и возвращение этого в JSON
    """
    if request.method == "GET":
        current_user = get_user(request).username
        data = view_in_wishlist(request, current_user)
        if data:
            return JsonResponse(data, json_dumps_params={'ensure_ascii': False})

        return JsonResponse({"answer": "Пользователь не авторизирован"}, status=404,
                            json_dumps_params={'ensure_ascii': False})


def home_view(request):
    """
    Представление для главной страницы
    """
    return render(request, 'wishlist/wishlist.html')