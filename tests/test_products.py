from django.test import TestCase, RequestFactory
from django.urls import reverse
from products.models import Product, Category
from products.views import product_list, product_detail


class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Electronics')
        self.product = Product.objects.create(
            name='Laptop',
            description='A powerful laptop',
            price=1000,
            in_stock=True,
            category=self.category
        )

    def test_product_creation(self):
        self.assertTrue(isinstance(self.product, Product))
        self.assertEqual(str(self.product), self.product.name)


class ProductListViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.category = Category.objects.create(name='Electronics', slug='electronics')

        self.product1 = Product.objects.create(
            name='Laptop',
            description='A powerful laptop',
            price=1000,
            in_stock=True,
            category=self.category
        )

        self.product2 = Product.objects.create(
            name='Phone',
            description='A smartphone',
            price=800,
            in_stock=True,
            category=self.category
        )

    def test_product_list_view(self):
        url = reverse('products:product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Laptop')
        self.assertContains(response, 'Phone')

    def test_product_list_filter_by_category(self):
        url = reverse('products:product-list-by-category', args=[self.category.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Laptop')
        self.assertNotContains(response, 'Nonexistent Product')

    def test_product_list_search_query(self):
        url = reverse('products:product-list')
        response = self.client.get(f'{url}?q=laptop')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Laptop')
        self.assertNotContains(response, 'Phone')

    def test_product_list_sorting(self):
        url = reverse('products:product-list')
        # По возрастанию цены
        response = self.client.get(f'{url}?sort=price_asc')
        products = list(response.context['products'])
        prices = [p.price for p in products]
        self.assertEqual(prices, sorted(prices))

        # По убыванию цены
        response = self.client.get(f'{url}?sort=price_desc')
        products = list(response.context['products'])
        prices = [p.price for p in products]
        self.assertEqual(prices, sorted(prices, reverse=True))


class ProductDetailViewTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Electronics')
        self.product = Product.objects.create(
            name='Laptop',
            description='A powerful laptop',
            price=1000,
            in_stock=True,
            category=self.category
        )

    def test_product_detail_view(self):
        url = reverse('products:product-detail', args=[self.product.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'A powerful laptop')
