from django.test import TestCase
from .models import *

class TestSystem(TestCase):

    def test_food_creation(self):
        c = Category.objects.create(name="Test")
        f = FoodItem.objects.create(name="Pizza", price=10, category=c)
        self.assertEqual(f.price, 10)

    def test_invoice(self):
        user = User.objects.create_user(username="user1", password="password")
        c = Category.objects.create(name="Food")
        f = FoodItem.objects.create(name="Burger", price=5, category=c)

        order = Order.objects.create(customer=user)
        OrderItem.objects.create(order=order, food_item=f, quantity=2)

        invoice = Invoice.objects.create(order=order, total_amount=10)

        self.assertEqual(invoice.total_amount, 10)

    def test_login_user(self):
        user = User.objects.create_user(username="user1", password="password", role="customer")
        self.client.login(username="user1", password="password")
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)