from django.test import TestCase
from .models import Products
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
# Create your tests here.

class ProductModelTest(TestCase):
    def test_product_creation(self):
        product=Products.objects.create(name='paracetamol',category="Pharmacy",price=50,  description="Pain relief", stock=100,is_active=True)

        self.assertEqual(product.name,'paracetamol')
        self.assertEqual(product.category, "Pharmacy")
        self.assertEqual(product.price,50)
        self.assertTrue(product.is_active)

    def test_product_str(self):
        product=Products.objects.create( name='Dolo',category="Pharmacy",price=30,stock=20)

        self.assertEqual(str(product), 'Dolo')

class ProductApiTest(APITestCase):
    def setUp(self):
        self.active_product=Products.objects.create(
            name="panadol",category="Pharmacy",price=50,  description="Pain relief", stock=100,is_active=True)
        
    
    def test_get_product_list(self):
        url=reverse('product-list')
        response=self.client.get(url)

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(len(response.data),1)
    
    def test_product_list_response_fields(self):
        url = reverse("product-list")
        response = self.client.get(url)

        product = response.data[0]

        self.assertIn("id", product)
        self.assertIn("name", product)
        self.assertIn("category", product)
        self.assertIn("price", product)
        self.assertIn("stock", product)
        self.assertIn("description", product)
        self.assertIn("image", product)
        self.assertIn("isActive", product)
        self.assertIn("created_at", product)

    def test_get_product_detail_success(self):
        url = reverse("product-detail", args=[self.active_product.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.active_product.name)