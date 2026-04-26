from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *

def user_login(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user:
            login(request, user)
            return redirect('/')
    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('/login/')


@login_required
def dashboard(request):
    if request.user.role == "customer":
        orders = Order.objects.filter(customer=request.user)
    else:
        orders = Order.objects.all()
    return render(request, 'dashboard.html', {'orders': orders})


@login_required
def create_order(request):
    items = FoodItem.objects.all()

    if request.method == "POST":
        order = Order.objects.create(customer=request.user)

        for item in items:
            qty = int(request.POST.get(f'item_{item.id}', 0))
            if qty > 0:
                OrderItem.objects.create(order=order, food_item=item, quantity=qty)

        return redirect('/')

    return render(request, 'order.html', {'items': items})


@login_required
def create_invoice(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if hasattr(order, 'invoice'):
        return redirect('/')

    items = OrderItem.objects.filter(order=order)
    total = sum(i.quantity * i.food_item.price for i in items)

    invoice = Invoice.objects.create(order=order, total_amount=total)

    for i in items:
        InvoiceItem.objects.create(
            invoice=invoice,
            food_item=i.food_item,
            quantity=i.quantity,
            price=i.food_item.price
        )

    return render(request, 'invoice.html', {'invoice': invoice})


@login_required
def update_order(request, order_id):
    order = Order.objects.get(id=order_id)

    if request.user.role != "staff":
        return redirect('/')

    order.status = "Delivered"
    order.save()

    return redirect('/')