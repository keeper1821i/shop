from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from app_shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm


# @require_POST
def cart_add(request, product_id):
    """"
    Добавляем товар в карзину
    """""
    if request.method == 'POST':
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cart.add(product=product,
                     quantity=cd['quantity'],
                     update_quantity=cd['update'])
        return redirect(f'/product_detail/{product_id}')
    else:
        form = CartAddProductForm()
        return render(request, 'shop/product_detail.html', {'form': form})


def cart_add_not_form(request, product_id):
    """"
    добавлять товар в корзину без заполнения формы
    """""
    cart = Cart(request)
    product = Product.objects.get(id=product_id)
    cart.add(product=product,
             quantity=1,
             update_quantity=False)
    return redirect(request.META.get('HTTP_REFERER'))


def cart_update(request, product_id):
    """"
    Обновить корзину
    """""
    cart = Cart(request)
    product = Product.objects.get(id=product_id)
    cart.update(product=product, update_quantity=False, quantity=1)
    return redirect('/cart/')


def cart_delete(request, product_id):
    """"
    Удалить товар из корзины
    """""
    cart = Cart(request)
    product = Product.objects.get(id=product_id)
    cart.update(product=product, update_quantity=True, quantity=1)
    return redirect('/cart/')


def cart_remove(request, product_id):
    """"
    Обнулить корзину
    """""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('/cart/')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],
                                                                   'update': True})

    return render(request, 'cart.html', {'cart': cart, })
