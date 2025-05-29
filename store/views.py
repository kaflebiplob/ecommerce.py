from django.shortcuts import render
from .models import *

def store(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'store/store.html', context)

def cart(request):
    items = []
    total_price = 0
    total_quantity = 0

    if request.user.is_authenticated:
        customer = request.user.customer
        orders = Order.objects.filter(customer=customer)

        for order in orders:
            order_items = order.orderitem_set.all()
            items.extend(order_items)

            for item in order_items:
                total_price += item.product.price * item.quantity
                total_quantity += item.quantity
    else:
     
        order = {'get_cart_total': 0, 'get_total_items': 0}

    # Construct fake order summary
    order = {
        'get_cart_total': total_price,
        'get_total_items': total_quantity
    }

    context = {'items': items, 'order': order}
    return render(request, 'store/cart.html', context)


def checkout(request):
     
    items = []
    total_price = 0
    total_quantity = 0

    if request.user.is_authenticated:
        customer = request.user.customer
        orders = Order.objects.filter(customer=customer)

        for order in orders:
            order_items = order.orderitem_set.all()
            items.extend(order_items)

            for item in order_items:
                total_price += item.product.price * item.quantity
                total_quantity += item.quantity
    else:
     
        order = {'get_cart_total': 0, 'get_total_items': 0}

    # Construct fake order summary
    order = {
        'get_cart_total': total_price,
        'get_total_items': total_quantity
    }

    context = {'items': items, 'order': order}
    
    return render(request, 'store/checkout.html', context)

