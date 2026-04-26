from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *

def user_login(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get('username'),
            password=request.POST.get('password')
        )

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'login.html', {'error': 'Invalid login'})

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

    invoice, created = Invoice.objects.get_or_create(
        order=order,
        defaults={'total_amount': 0}
    )

    if created:
        items = OrderItem.objects.filter(order=order)

        total = sum(i.quantity * i.food_item.price for i in items)
        invoice.total_amount = total
        invoice.save()

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

    order = get_object_or_404(Order, id=order_id)

    if request.user.role != "staff":
        return redirect('/')

    if request.method == "POST":
        order.status = request.POST.get("status")
        order.save()

    return render(request, 'update_order.html', {'order': order})


@login_required
def admin_dashboard(request):

    if request.user.role != "manager":
        return redirect('/')

    total_orders = Order.objects.count()
    total_revenue = sum(i.total_amount for i in Invoice.objects.all())
    pending_orders = Order.objects.filter(status="Pending").count()

    return render(request, 'admin_dashboard.html', {
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'pending_orders': pending_orders
    })

@login_required
def staff_dashboard(request):

    if request.user.role != "staff":
        return redirect('/')

    orders = Order.objects.exclude(status="Delivered")

    return render(request, 'staff_dashboard.html', {'orders': orders})