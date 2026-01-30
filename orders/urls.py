from django.urls import path
from . import views

urlpatterns = [
    path('stul/<int:table_number>/<str:token>/', views.table_detail, name='table_detail'),
    path('zamestnanec/', views.staff_dashboard, name='staff_dashboard'),
    
    path('order/<int:order_id>/<str:action>/', views.order_action, name='order_action'),
]