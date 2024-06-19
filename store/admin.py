from django.contrib import admin
from .models import (Product, ProductType, ProductAttribute,
                     ProductAttributeValue, CartItem, Cart, Order, OrderItem, Brand, Application)


# Register your models here.

class ProductAttributeValueInline(admin.TabularInline):
    model = ProductAttributeValue
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_type', 'price', 'stock',)
    list_filter = ('price', 'product_type', 'brand')
    search_fields = ('name', 'description', 'product_type', 'brand')
    inlines = [ProductAttributeValueInline]


class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 1


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [ProductAttributeInline]


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


# ProductAttribute Admin
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_type')
    list_filter = ('product_type',)


# ProductAttributeValue Admin
class ProductAttributeValueAdmin(admin.ModelAdmin):
    list_display = ('product', 'attribute', 'value')
    list_filter = ('attribute',)
    search_fields = ('product__name', 'attribute__name', 'value')




class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1


class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    inlines = [CartItemInline]


class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity')
    search_fields = ('cart__user__username', 'product__name')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'address', 'phone_number', 'status', 'total_price', 'created_at')
    list_filter = ('status', 'created_at')
    inlines = [OrderItemInline]


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')
    search_fields = ('price', 'product__name', 'order__created_at')


class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    list_filter = ('name',)


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')




admin.site.register(Product, ProductAdmin)
admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(ProductAttribute, ProductAttributeAdmin)
admin.site.register(ProductAttributeValue, ProductAttributeValueAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Application, ApplicationAdmin)
