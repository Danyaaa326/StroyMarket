from django.contrib import admin
from .models import Cart, CartItem, Order

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at']
    list_filter = ['created_at']

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'cart', 'product', 'quantity', 'get_cost']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'phone', 'total', 'created_at', 'status']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'phone', 'email']
    readonly_fields = ['created_at']