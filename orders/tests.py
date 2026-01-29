from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from .models import Table, Product, ProductType, Order

class OrderBusinessLogicTest(TestCase):
    def setUp(self):
        """Příprava dat pro každý test."""
        self.table = Table.objects.create(number=1)
        self.drink = Product.objects.create(name='Káva')
        self.espresso = ProductType.objects.create(product=self.drink, name='Espresso')

    def test_new_order_is_pending(self):
        """Test: Nová objednávka má status 'Nová'."""
        order = Order.objects.create(table=self.table, product_type=self.espresso)
        self.assertEqual(order.calculated_status, 'Nová')

    def test_missed_order_logic(self):
        """Test: Pokud se objednávka nepřijme do 10 min, je 'Propáslá'."""
        order = Order.objects.create(table=self.table, product_type=self.espresso)
        
        past_time = timezone.now() - timedelta(minutes=11)
        Order.objects.filter(pk=order.pk).update(created_at=past_time)
        
        order.refresh_from_db()
        self.assertEqual(order.calculated_status, 'Propáslá')

    def test_not_finished_order_logic(self):
        """Test: Pokud se objednávka nedokončí do 15 min od přijetí, je 'Nestihnutá'."""
        order = Order.objects.create(table=self.table, product_type=self.espresso)
        order.accept()
        
        past_accepted = timezone.now() - timedelta(minutes=16)
        Order.objects.filter(pk=order.pk).update(accepted_at=past_accepted)
        
        order.refresh_from_db()
        self.assertEqual(order.calculated_status, 'Nestihnutá')

    def test_complete_rejected_order_fail(self):
        """Test: Nelze dokončit odmítnutou objednávku."""
        order = Order.objects.create(table=self.table, product_type=self.espresso)
        order.reject()
        order.complete()
        
        self.assertEqual(order.status, 'REJECTED')

    def test_sync_status(self):
        """Test: Ověření, že změna stavu se projeví (simulace synchronizace)."""
        order = Order.objects.create(table=self.table, product_type=self.espresso)
        self.assertEqual(order.calculated_status, 'Nová')
        
        order.accept()
        self.assertEqual(order.calculated_status, 'Přijatá')
        
        order.complete()
        self.assertEqual(order.calculated_status, 'Dokončená')