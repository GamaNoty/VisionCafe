from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Table, Order, ProductType

def table_detail(request, table_number):
    table = get_object_or_404(Table, number=table_number)
    
    if request.method == 'POST':
        product_type_id = request.POST.get('product_type')
        if product_type_id:
            Order.objects.create(
                table=table,
                product_type_id=product_type_id,
                status='PENDING'
            )
            return redirect('table_detail', table_number=table.number)

    product_types = ProductType.objects.all() 
    orders = Order.objects.filter(table=table).order_by('-created_at')

    context = {
        'table': table,
        'product_types': product_types,
        'orders': orders,
        'full_url': request.build_absolute_uri(),
    }
    return render(request, 'orders/table_detail.html', context)

@login_required
def staff_dashboard(request):
    all_orders = Order.objects.all().order_by('-created_at')
    return render(request, 'orders/staff_dashboard.html', {'orders': all_orders})

@login_required
def order_action(request, order_id, action):
    order = get_object_or_404(Order, id=order_id)
    if action == 'accept':
        order.accept()
    elif action == 'reject':
        order.reject()
    elif action == 'complete':
        order.complete()
    return redirect('staff_dashboard')