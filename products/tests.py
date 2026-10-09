from django.test import TestCase
from rest_framework.test import APIClient
from .models import Category, Product


class CategoryTestCase(TestCase):
    def setUp(self):
        from django.contrib.auth import get_user_model

        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username='tester_category', password='secret123'
        )
        self.client.force_authenticate(user=self.user)
        self.category = Category.objects.create(name='Electronica')

    def test_create_category(self):
        response = self.client.post('/api/v1/categories/', {'name': 'Ropa'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Category.objects.count(), 3)

    def test_list_categories(self):
        response = self.client.get('/api/v1/categories/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)


class ProductTestCase(TestCase):
    def setUp(self):
        from django.contrib.auth import get_user_model

        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username='tester_product', password='secret123'
        )
        self.client.force_authenticate(user=self.user)
        self.category = Category.objects.create(name='Electronica')
        self.product = Product.objects.create(
            name='Laptop',
            category=self.category,
            description='Laptop HP',
            price=15000.00,
        )

    def test_create_product(self):
        response = self.client.post('/api/v1/products/', {
            'name': 'Mouse',
            'category_id': self.category.id,
            'description': 'Mouse inalambrico',
            'price': 500.00,
        })
        self.assertEqual(response.status_code, 201)

    def test_list_products(self):
        response = self.client.get('/api/v1/products/')
        self.assertEqual(response.status_code, 200)

    def test_update_product(self):
        response = self.client.put(f'/api/v1/products/{self.product.id}/', {
            'name': 'Laptop Pro',
            'category_id': self.category.id,
            'description': 'Laptop HP actualizada',
            'price': 18000.00,
        })
        self.assertEqual(response.status_code, 200)

    def test_delete_product(self):
        response = self.client.delete(f'/api/v1/products/{self.product.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Product.objects.count(), 0)
    
    def test_precio_final_autenticado(self):
        response = self.client.get(f'/api/v1/products/{self.product.id}/precio-final/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('precio_final', response.data)

    def test_precio_final_sin_autenticar(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(f'/api/v1/products/{self.product.id}/precio-final/')
        self.assertEqual(response.status_code, 401)

    