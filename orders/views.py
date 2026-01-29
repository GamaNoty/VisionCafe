from django.shortcuts import render, get_object_or_404, redirect
from .models import Table, Order, ProductType

def table_detail(request, table_number):
    table = get_object_or_404(Table, number=table_number)
    
    if request.method == 'POST':
        product_type_id = request.POST.get('product_type')
        if product_type_id:
            Order.objects.create(
                table=table,
                product_type_id=product_type_id
            )
            return redirect('table_detail', table_number=table.number)

    orders = Order.objects.filter(table=table).order_by('-created_at')
    product_types = ProductType.objects.all()
    
    context = {
        'table': table,
        'orders': orders,
        'product_types': product_types,
        'full_url': request.build_absolute_uri(),
    }
    return render(request, 'orders/table_detail.html', context)