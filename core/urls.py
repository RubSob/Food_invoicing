from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard),
    path('login/', views.user_login),
    path('logout/', views.user_logout),
    path('order/', views.create_order),
    path('invoice/<int:order_id>/', views.create_invoice),
    path('update/<int:order_id>/', views.update_order),
]