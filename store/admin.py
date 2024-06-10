from django.contrib import admin
from .models import Product, ProductType, ProductAttribute, ProductAttributeValue, CartItem, Cart


# Register your models here.

class ProductAttributeValueInline(admin.TabularInline):
    model = ProductAttributeValue
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_type', 'price', 'stock')
    list_filter = ('price', 'product_type')
    search_fields = ('name', 'description', 'product_type')
    inlines = [ProductAttributeValueInline]


class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 1


class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [ProductAttributeInline]


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


# ProductAttribute Admin
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_type')


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


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(ProductAttribute, ProductAttributeAdmin)
admin.site.register(ProductAttributeValue, ProductAttributeValueAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
