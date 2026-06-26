from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    # Customer routes
    path('customer/dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('customer/order/create/', views.create_order, name='create_order'),
    
    # Driver routes
    path('driver/dashboard/', views.driver_dashboard, name='driver_dashboard'),
    path('driver/order/<int:order_id>/status/', views.update_status, name='update_status'),
    
    # Admin routes
    path('admin-ops/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-ops/order/<int:order_id>/assign/', views.assign_driver, name='assign_driver'),
    
    # Custom Admin CRUD - Users
    path('admin-ops/user/create/', views.admin_create_user, name='admin_create_user'),
    path('admin-ops/user/<int:user_id>/edit/', views.admin_edit_user, name='admin_edit_user'),
    path('admin-ops/user/<int:user_id>/delete/', views.admin_delete_user, name='admin_delete_user'),
    
    # Custom Admin CRUD - Orders
    path('admin-ops/order/create/', views.admin_create_order, name='admin_create_order'),
    path('admin-ops/order/<int:order_id>/edit/', views.admin_edit_order, name='admin_edit_order'),
    path('admin-ops/order/<int:order_id>/delete/', views.admin_delete_order, name='admin_delete_order'),
]
