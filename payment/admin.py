from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'quantity', 'price', 'user']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'email',
                    'amount_paid', 'date_ordered', 'status']
    list_filter = ['status', 'date_ordered']
    search_fields = ['full_name', 'email', 'id']
    readonly_fields = ['full_name', 'email',
                       'shipping_address', 'amount_paid', 'date_ordered', 'user']
    list_editable = ['status']  # Make status editable directly from list view
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product', 'quantity', 'price', 'user']
    list_filter = ['order__status']
    search_fields = ['order__id', 'product__name']
    readonly_fields = ['order', 'product', 'quantity', 'price', 'user']


admin.site.register(ShippingAddress)
