    from django.test import TestCase
    from django.urls import reverse
    from .models import *

    class TestSystem(TestCase):

        def test_food_creation(self):  #unit
            c = Category.objects.create(name="Test")
            f = FoodItem.objects.create(name="Pizza", price=10, category=c)
            self.assertEqual(f.price, 10)

        def test_invoice_model(self):   #unit
            user = User.objects.create_user(username="user1", password="password", role="customer")
            c = Category.objects.create(name="Food")
            f = FoodItem.objects.create(name="Burger", price=5, category=c)

            order = Order.objects.create(customer=user)
            OrderItem.objects.create(order=order, food_item=f, quantity=2)

            invoice = Invoice.objects.create(order=order, total_amount=10)

            self.assertEqual(invoice.total_amount, 10)


        def test_order_to_invoice_flow(self):
            user = User.objects.create_user(username="user1", password="password", role="customer")
            c = Category.objects.create(name="Food")
            f = FoodItem.objects.create(name="Burger", price=5, category=c)

            order = Order.objects.create(customer=user)
            OrderItem.objects.create(order=order, food_item=f, quantity=3)

            total = sum(i.quantity * i.food_item.price for i in OrderItem.objects.filter(order=order))
            invoice = Invoice.objects.create(order=order, total_amount=total)

            self.assertEqual(invoice.total_amount, 15)





        def test_login_user(self):
            user = User.objects.create_user(username="user1", password="password", role="customer")
            login = self.client.login(username="user1", password="password")
            self.assertTrue(login)

            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)


        def test_customer_create_order(self):
            user = User.objects.create_user(username="user1", password="password", role="customer")
            self.client.login(username="user1", password="password")

            c = Category.objects.create(name="Food")
            f = FoodItem.objects.create(name="Pizza", price=10, category=c)

            response = self.client.post('/order/', {
                f'item_{f.id}': 2
            })

            self.assertEqual(response.status_code, 302)  # redirect after success
            self.assertEqual(Order.objects.count(), 1)


        def test_invoice_generation_view(self):
            user = User.objects.create_user(username="user1", password="password", role="customer")
            self.client.login(username="user1", password="password")

            c = Category.objects.create(name="Food")
            f = FoodItem.objects.create(name="Burger", price=5, category=c)

            order = Order.objects.create(customer=user)
            OrderItem.objects.create(order=order, food_item=f, quantity=2)

            response = self.client.get(f'/invoice/{order.id}/')

            self.assertEqual(response.status_code, 200)
            self.assertTrue(Invoice.objects.filter(order=order).exists())


        def test_staff_can_update_order(self):
            staff = User.objects.create_user(username="staff", password="password", role="staff")
            customer = User.objects.create_user(username="user1", password="password", role="customer")

            order = Order.objects.create(customer=customer)

            self.client.login(username="staff", password="password")

            response = self.client.post(f'/update/{order.id}/', {'status': 'Delivered'})

            order.refresh_from_db()
            self.assertEqual(order.status, "Delivered")


        def test_customer_cannot_update_order(self):
            user = User.objects.create_user(username="user1", password="password", role="customer")

            order = Order.objects.create(customer=user)

            self.client.login(username="user1", password="password")

            response = self.client.post(f'/update/{order.id}/', {'status': 'Delivered'})

            order.refresh_from_db()
            self.assertNotEqual(order.status, "Delivered")


        def test_manager_dashboard_access(self):
            manager = User.objects.create_user(username="admin", password="password", role="manager")
            self.client.login(username="admin", password="password")

            response = self.client.get('/admin-dashboard/')
            self.assertEqual(response.status_code, 200)


        def test_staff_dashboard_access(self):
            staff = User.objects.create_user(username="staff", password="password", role="staff")
            self.client.login(username="staff", password="password")

            response = self.client.get('/staff-dashboard/')
            self.assertEqual(response.status_code, 200)