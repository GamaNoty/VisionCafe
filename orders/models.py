from django.db import models
from django.utils import timezone
from datetime import timedelta

class Table(models.Model):
    number = models.IntegerField(unique=True)
    
    def __str__(self):
        return f"Stůl {self.number}"

class Product(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class ProductType(models.Model):
    product = models.ForeignKey(Product, related_name='types', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.product.name} - {self.name}"

class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Nová'),
        ('ACCEPTED', 'Přijatá'),
        ('REJECTED', 'Odmítnutá'),
        ('COMPLETED', 'Dokončená'),
    ]

    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    
    created_at = models.DateTimeField(auto_now_add=True)
    accepted_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    @property
    def calculated_status(self):
        now = timezone.now()
        if self.status == 'PENDING' and now > self.created_at + timedelta(minutes=10):
            return 'Propáslá'
        
        if self.status == 'ACCEPTED' and self.accepted_at and now > self.accepted_at + timedelta(minutes=15):
            return 'Nestihnutá'
        return self.get_status_display()
    
    def accept(self):
        """Zaměstnanec přijímá objednávku."""
        if self.status == 'PENDING':
            self.status = 'ACCEPTED'
            self.accepted_at = timezone.now()
            self.save()

    def reject(self):
        """Zaměstnanec odmítá objednávku."""
        if self.status == 'PENDING':
            self.status = 'REJECTED'
            self.save()

    def complete(self):
        """Zaměstnanec dokončuje objednávku."""
        if self.status == 'ACCEPTED':
            self.status = 'COMPLETED'
            self.completed_at = timezone.now()
            self.save()
