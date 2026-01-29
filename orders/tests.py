from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from .models import Table, Product, ProductType, Order

class OrderLogicTest(TestCase):
    def setUp(self):
        self.table = Table.objects.create(number=1)
        self.tea = Product.objects.create(name='Čaj')
        self.green_tea = ProductType.objects.create(product=self.tea, name='Zelený')

    def test_missed_order(self):
        """Test: Objednávka po 10 minutách bez přijetí je 'Propáslá'."""
        order = Order.objects.create(table=self.table, product_type=self.green_tea)
        # Ruční posun času v DB
        Order.objects.filter(id=order.id).update(created_at=timezone.now() - timedelta(minutes=11))
        order.refresh_from_db()
        self.assertEqual(order.calculated_status, 'Propáslá')

    def test_overdue_order(self):
        """Test: Přijatá objednávka po 15 minutách je 'Nestihnutá'."""
        order = Order.objects.create(table=self.table, product_type=self.green_tea, status='ACCEPTED', accepted_at=timezone.now() - timedelta(minutes=16))
        self.assertEqual(order.calculated_status, 'Nestihnutá')