from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Table, Order, Product, ProductType
from django.http import Http404
from django.urls import reverse

def table_detail(request, table_number, token):
    table = get_object_or_404(Table, number=table_number)
    
    current_token = table.get_current_token()
    
    if request.method == 'POST':
        product_type_id = request.POST.get('product_type')
        if product_type_id:
            Order.objects.create(
                table=table,
                product_type_id=product_type_id,
                status='PENDING'
            )
            return redirect('table_detail', table_number=table.number, token=current_token)

    products = Product.objects.all().prefetch_related('types')
    orders = Order.objects.filter(table=table).order_by('-created_at')

    full_url = request.build_absolute_uri(
        reverse('table_detail', args=[table.number, current_token])
    )

    context = {
        'table': table,
        'products': products,
        'orders': orders,
        'full_url': full_url,
    }
    
    return render(request, 'orders/table_detail.html', context)

@login_required
@staff_member_required
def staff_dashboard(request):
    all_orders = Order.objects.all().order_by('-created_at')
    return render(request, 'orders/staff_dashboard.html', {'orders': all_orders})
    orders = Order.objects.all().order_id('-created_at')

@login_required
@staff_member_required
def order_action(request, order_id, action):
    order = get_object_or_404(Order, id=order_id)
    if action == 'accept':
        order.accept()
    elif action == 'reject':
        order.reject()
    elif action == 'complete':
        order.complete()
    return redirect('staff_dashboard')