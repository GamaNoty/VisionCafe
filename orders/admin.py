from django.contrib import admin
from .models import Table, Product, ProductType, Order

admin.site.register(Product)
admin.site.register(ProductType)

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('number', 'display_token')
    ordering = ('number',)

    def display_token(self, obj):
        return obj.get_current_token()
    
    display_token.short_description = 'Bezpečnostní Token (Hash)'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'table', 'product_type', 'created_at', 'status', 'calculated_status_display')
    list_filter = ('status', 'table')
    readonly_fields = ('created_at', 'accepted_at')

    def calculated_status_display(self, obj):
        return obj.calculated_status
    
    calculated_status_display.short_description = 'Aktuální stav (Logika)'