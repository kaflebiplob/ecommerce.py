from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json

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

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    
    print('Action:', action)
    print('Product:', productId)
    
    user = request.user
    customer = user.customer
    product = Product.objects.get(id=productId)
    
    # Handle multiple incomplete orders - get or create the most recent one
    try:
        order = Order.objects.filter(customer=customer, complete=False).latest('date_ordered')
    except Order.DoesNotExist:
        order = Order.objects.create(customer=customer, complete=False)
    
    # Alternative approach: Clean up duplicates and then get_or_create
    # Order.objects.filter(customer=customer, complete=False).exclude(
    #     id=Order.objects.filter(customer=customer, complete=False).latest('date_ordered').id
    # ).delete()
    # order, created = Order.objects.get_or_create(customer=customer, complete=False)
    
    orderItem, created = OrderItem.objects.get_or_create(
        order=order,
        product=product,
        defaults={'quantity': 0}
    )
    
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    
    orderItem.save()
    
    if orderItem.quantity <= 0:
        orderItem.delete()
    
    return JsonResponse('Item was added', safe=False)