from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('customer/dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('delivery/dashboard/', views.delivery_dashboard, name='delivery_dashboard'),
    path('delivery/order/<uuid:order_id>/<str:action>/', views.delivery_update_status, name='delivery_update_status'),
    path('profile/', views.profile, name='profile'),
    path('auth/phone/request-otp/', views.request_phone_otp, name='request_phone_otp'),
    path('auth/phone/verify/', views.verify_phone_otp, name='verify_phone_otp'),
    path('order/<uuid:order_id>/cancel/', views.cancel_order, name='cancel_order'),
    path('order/<uuid:order_id>/', views.order_details, name='order_details'),
    path('order/<uuid:order_id>/pay/', views.pay_order, name='pay_order'),
    path('restaurant/list/', views.restaurant_list, name='restaurant_list'),
    path('restaurant/<int:pk>/', views.restaurant_detail, name='restaurant_detail'),
    path('restaurant/<int:restaurant_id>/upload-image/', views.upload_restaurant_image, name='upload_restaurant_image'),
    path('search/', views.search, name='search'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    # Address
    path('address/add/', views.add_address, name='add_address'),
    path('address/<int:address_id>/delete/', views.delete_address, name='delete_address'),
    # Cart
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/clear/', views.clear_cart, name='clear_cart'),
    path('cart/add/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    # Checkout
    path('checkout/', views.checkout, name='checkout'),
]