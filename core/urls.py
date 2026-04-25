from django.urls import path
from . import views

urlpatterns = [
    path('', views.invoice_list, name='invoice_list'),
    path('create/', views.create_invoice, name='create_invoice'),
    path('<int:invoice_id>/', views.invoice_detail, name='invoice_detail'),
    path('<int:invoice_id>/add_item/', views.add_item, name='add_item'),
    path('<int:invoice_id>/paid/', views.mark_paid, name='mark_paid'),

    path('products/', views.product_list, name='product_list'),
    path('products/create/', views.create_product, name='create_product'),
]