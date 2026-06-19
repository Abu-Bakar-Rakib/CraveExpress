from django.contrib import admin
from .models import (
    User,
    Address,
    Restaurant,
    MenuItem,
    DeliveryPersonnel,
    DeliverySchedule,
    Order,
    OrderItem,
    Payment,
    ServiceableArea,
)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'user_type', 'is_active')
    list_filter = ('user_type', 'is_active')
    search_fields = ('username', 'email', 'phone_number')


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'postal_code', 'is_default', 'is_serviceable')
    list_filter = ('city', 'is_serviceable')
    search_fields = ('address_line', 'city', 'postal_code')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'customer', 'restaurant', 'status', 'payment_method', 'total_amount', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('order_id', 'customer__username', 'restaurant__name')
    inlines = [OrderItemInline]


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant', 'price', 'is_available')
    list_filter = ('restaurant', 'is_available')
    search_fields = ('name',)


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'email', 'opening_time', 'closing_time')
    search_fields = ('name',)


@admin.register(DeliveryPersonnel)
class DeliveryPersonnelAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_available')
    list_filter = ('is_available',)


@admin.register(DeliverySchedule)
class DeliveryScheduleAdmin(admin.ModelAdmin):
    list_display = ('delivery_person', 'date', 'start_time', 'end_time')
    list_filter = ('date',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'payment_id', 'amount', 'payment_method', 'status', 'created_at')
    list_filter = ('status', 'payment_method')
    search_fields = ('payment_id', 'transaction_id')


@admin.register(ServiceableArea)
class ServiceableAreaAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_filter = ('is_active',)
