from django.shortcuts import render, get_object_or_404
from store.models import Product
from .cart import Cart
from django.http import JsonResponse
from decimal import Decimal


# Create your views here.


def cart_summary(request):
    cart = Cart(request)

    return render(request, 'cart/cart-summary.html', {'cart': cart})


def cart_add(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_quantity = int(request.POST.get('product_quantity'))

        product = get_object_or_404(Product, id=product_id)

        # Check if enough inventory is available
        if product.quantity >= product_quantity:
            cart.add(product=product, product_qty=product_quantity)
            cart_quantity = cart.__len__()
            response = JsonResponse({'qty': cart_quantity, 'success': True})
        else:
            response = JsonResponse({
                'success': False,
                'message': f'Sorry, only {product.quantity} items available'
            })

        return response


def cart_delete(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))

        cart.delete(product=product_id)

        cart_quantity = cart.__len__()

        cart_total = cart.get_total()

        response = JsonResponse({'qty': cart_quantity, 'total': cart_total})

        return response


def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_quantity = int(request.POST.get('product_quantity'))

        product = get_object_or_404(Product, id=product_id)

        # Inventory check
        if product_quantity > product.quantity:
            return JsonResponse({
                'success': False,
                'message': f'Sorry, only {product.quantity} items available'
            })
        elif product_quantity <= 0:
            return JsonResponse({
                'success': False,
                'message': 'Quantity must be at least 1'
            })

        cart.update(product=product_id, qty=product_quantity)
        cart_quantity = cart.__len__()
        cart_total = cart.get_total()

        return JsonResponse({
            'success': True,
            'qty': cart_quantity,
            'total': cart_total,
            'new_qty': product_quantity,
            'product_quantity': product.quantity,
            'product_price': str(product.price)
        })