from django.db import models

from django.conf import settings

from django.contrib.auth.models import User

import cart


# Create your models here.


class ProductType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField()
    stock = models.IntegerField()
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    availability = models.BooleanField(default=True)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.name


class ProductAttribute(models.Model):
    name = models.CharField(max_length=100)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class ProductAttributeValue(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_values')
    attribute = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE, related_name='attribute_values')
    value = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.attribute.name}: {self.value}"


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart {self.id} for {self.user.email}"

    def __iter__(self):
        return iter(self.items.all())


class Favourites(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='favourites')
    created_at = models.DateTimeField(auto_now_add=True)


class FavouriteItem(models.Model):
    favourites_list = models.ForeignKey(Favourites, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

    def get_total_price(self):
        return self.quantity * self.product.price


class Order(models.Model):
    class Delivery(models.TextChoices):
        courier = 'Courier'
        pickup = 'Pickup'

    class Payment(models.TextChoices):
        card = 'Card', 'card'
        cash = 'Cash', 'cash'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    name = models.CharField(max_length=100, default='')
    address = models.CharField(max_length=100, default='')
    phone_number = models.CharField(max_length=100, default='')
    delivery_option = models.CharField(max_length=100, choices=Delivery.choices, default=Delivery.courier)
    payment_option = models.CharField(max_length=100, choices=Payment.choices, default=Payment.card)
    #above user data
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.id}: {self.user}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in order {self.order.id}"

    def get_total_price(self):
        return self.quantity * self.price
