from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from .models import Category, Product

User = get_user_model()


class CategoryTestCase(TestCase):
	def setUp(self):
		self.client = APIClient()
		self.user = User.objects.create_user(
			email='test@example.com',
			password='test_password123',
		)
		self.client.force_authenticate(user=self.user)
		self.category = Category.objects.create(name='Electronica')

	def test_create_category(self):
		response = self.client.post('/api/categories/', {'name': 'Ropa'})

		self.assertEqual(response.status_code, 201)
		self.assertEqual(Category.objects.count(), 2)

	def test_list_categories(self):
		response = self.client.get('/api/categories/')

		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.data), 1)


class ProductTestCase(TestCase):
	def setUp(self):
		self.client = APIClient()
		self.user = User.objects.create_user(
			email='test@example.com',
			password='test_password123',
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
		response = self.client.post('/api/products/', {
			'name': 'Mouse',
			'category': self.category.id,
			'description': 'Mouse inalambrico',
			'price': 500.00,
		})

		self.assertEqual(response.status_code, 201)
		self.assertEqual(Product.objects.count(), 2)

	def test_list_products(self):
		response = self.client.get('/api/products/')

		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.data), 1)

	def test_update_product(self):
		response = self.client.put(
			f'/api/products/{self.product.id}/',
			{
				'name': 'Laptop Pro',
				'category': self.category.id,
				'description': 'Laptop HP actualizada',
				'price': 18000.00,
			},
		)

		self.assertEqual(response.status_code, 200)
		self.product.refresh_from_db()
		self.assertEqual(self.product.name, 'Laptop Pro')

	def test_delete_product(self):
		response = self.client.delete(f'/api/products/{self.product.id}/')

		self.assertEqual(response.status_code, 204)
		self.assertEqual(Product.objects.count(), 0)

	def test_precio_final_autenticado(self):
		response = self.client.get(
			f'/api/v1/products/{self.product.id}/precio-final/'
		)

		self.assertEqual(response.status_code, 200)
		self.assertIn('precio_final', response.data)
		self.assertEqual(response.data['precio_final'], 13500.00)

	def test_precio_final_sin_autenticar(self):
		self.client.force_authenticate(user=None)
		response = self.client.get(
			f'/api/v1/products/{self.product.id}/precio-final/'
		)

		self.assertEqual(response.status_code, 401)


class UserSecurityTestCase(TestCase):
	def setUp(self):
		self.client = APIClient()
		self.user = User.objects.create_user(
			email='ana@example.com', password='ClaveSegura123', carrera='Ingeniería'
		)
		self.client.force_authenticate(user=self.user)

	def test_personal_data_never_exposes_password_hash(self):
		response = self.client.get('/api/usuarios/datos-personales/')
		self.assertEqual(response.status_code, 200)
		self.assertNotIn('password', response.data)
		self.assertNotIn('pbkdf2', str(response.data))

	def test_update_without_password_keeps_existing_password(self):
		old_hash = self.user.password
		response = self.client.patch(
			f'/api/usuarios/{self.user.id}/', {'carrera': 'Arquitectura'}, format='json'
		)
		self.assertEqual(response.status_code, 200)
		self.user.refresh_from_db()
		self.assertEqual(self.user.password, old_hash)
		self.assertTrue(self.user.check_password('ClaveSegura123'))
		self.assertNotIn('password', response.data)

	def test_access_token_uses_email_and_is_configured(self):
		self.client.force_authenticate(user=None)
		response = self.client.post('/api/token/', {
			'email': 'ana@example.com', 'password': 'ClaveSegura123'
		}, format='json')
		self.assertEqual(response.status_code, 200)
		self.assertIn('access', response.data)
