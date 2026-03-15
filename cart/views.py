from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from main.models import Product
from .models import Cart, CartItem


@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart/detail.html', {'cart': cart})


@login_required
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 1}
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, f'Количество {product.name} увеличено')
    else:
        messages.success(request, f'{product.name} добавлен в корзину')

    return redirect('cart_detail')


@login_required
def cart_remove(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    product_name = cart_item.product.name
    cart_item.delete()
    messages.success(request, f'{product_name} удален из корзины')
    return redirect('cart_detail')


@login_required
def cart_update(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'Количество обновлено')
        else:
            cart_item.delete()
            messages.success(request, 'Товар удален')
    return redirect('cart_detail')


from django.http import JsonResponse
from .models import Order
import json


def create_order(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # Получаем корзину текущего пользователя
            cart = Cart.objects.get(user=request.user)

            # Собираем данные корзины для снимка
            cart_items = []
            for item in cart.items.all():
                cart_items.append({
                    'product_id': item.product.id,
                    'product_name': item.product.name,
                    'price': str(item.product.price),
                    'quantity': item.quantity,
                    'cost': str(item.get_cost())
                })

            # Создаём заказ
            order = Order.objects.create(
                user=request.user if request.user.is_authenticated else None,
                name=data.get('name'),
                phone=data.get('phone'),
                email=data.get('email'),
                comment=data.get('comment', ''),
                cart_data={
                    'items': cart_items,
                    'total': str(cart.get_total())
                },
                total=cart.get_total()
            )

            # Очищаем корзину после заказа
            cart.items.all().delete()

            return JsonResponse({'success': True, 'order_id': order.id})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Method not allowed'})