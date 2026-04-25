from django import forms
from .models import Invoice, Item, Product

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['customer']


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['product', 'quantity']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price']