from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib.auth.models import User

# HOME (LIST)
def invoice_list(request):
    invoices = Invoice.objects.all()
    return render(request, 'invoice/invoice_list.html', {'invoices': invoices})


def create_invoice(request):

    if not request.user.is_authenticated:
        return redirect('login')

    if request.user.username != "admin":
        return redirect('/')

    form = InvoiceForm(request.POST or None)

    if form.is_valid():
        invoice = form.save(commit=False)

        if request.user.is_authenticated:
            invoice.created_by = request.user
        else:
            invoice.created_by = User.objects.first()

        invoice.save()
        return redirect('invoice_list')

    return render(request, 'invoice/invoice_create.html', {'form': form})


# DETAIL
def invoice_detail(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    return render(request, 'invoice/invoice_detail.html', {'invoice': invoice})




def add_item(request, invoice_id):

    if not request.user.is_authenticated:
        return redirect('login')

    if request.user.username != "admin":
        return redirect('/')

    invoice = get_object_or_404(Invoice, id=invoice_id)

    form = ItemForm(request.POST or None)   # ✅ THIS WAS MISSING

    if form.is_valid():
        item = form.save(commit=False)
        item.invoice = invoice
        item.save()
        return redirect('invoice_detail', invoice_id=invoice.id)

    return render(request, 'invoice/add_item.html', {'form': form})




# MARK PAID
def mark_paid(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    invoice.is_paid = True
    invoice.save()
    return redirect('invoice_detail', invoice_id=invoice.id)


# PRODUCTS
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product/product_list.html', {'products': products})


def create_product(request):

    if not request.user.is_authenticated:
        return redirect('login')

    if request.user.username != "admin":
        return redirect('/')

    form = ProductForm(request.POST or None)
    
    if form.is_valid():
        form.save()
        return redirect('product_list')
    return render(request, 'product/product_create.html', {'form': form})