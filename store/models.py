from _decimal import Decimal
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['-pk']

    def __str__(self):
        return f'{self.name}'


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='product_name')
    code = models.CharField(max_length=255, verbose_name='product_code')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    image_url = models.ImageField(upload_to='static/images/')
    description = models.TextField()

    class Meta:
        ordering = ['-pk']

    def __str__(self):
        return f'{self.name} - {self.price}'


class Order(models.Model):
    STATUS_CART = 'cart'
    STATUS_WAITING_FOR_PAYMENT = 'waiting_for_payment'
    STATUS_PAID = 'paid'
    STATUS_SENT = 'sent'
    STATUS_CHOICES = [
        (STATUS_CART, 'cart'),
        (STATUS_WAITING_FOR_PAYMENT, 'waiting_for_payment'),
        (STATUS_PAID, 'paid'),
        (STATUS_SENT, 'sent'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default=STATUS_CART)
    amount = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    creation_time = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    phone_number = models.CharField(max_length=15, null=True)
    city = models.CharField(max_length=100, null=True)
    post_office = models.CharField(max_length=100, null=True)

    class Meta:
        ordering = ['-pk']

    def __str__(self):
        return f'{self.user} - {self.amount} - {self.status}'

    @staticmethod
    def get_cart(user: User):
        cart = Order.objects.filter(user=user, status=Order.STATUS_CART).first()
        if not cart:
            cart = Order.objects.create(user=user, status=Order.STATUS_CART, amount=0)
        return cart

    def get_amount(self):
        amount = Decimal(0)
        for item in self.orderitem_set.all():
            amount += item.amount
        return amount

    def make_order(self):
        items = self.orderitem_set.all()
        if items and self.status == Order.STATUS_CART:
            self.status = Order.STATUS_WAITING_FOR_PAYMENT
            self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=20, decimal_places=2)

    class Meta:
        ordering = ['-pk']

    def __str__(self):
        return f'{self.product} - {self.price} - {self.quantity} - {self.order.status}'

    @property
    def amount(self):
        return self.quantity * self.price


@receiver(post_save, sender=OrderItem)
def recalculate_order_amount_after_save(sender, instance, **kwargs):
    order = instance.order
    order.amount = order.get_amount()
    order.save()


@receiver(post_delete, sender=OrderItem)
def recalculate_order_amount_after_delete(sender, instance, **kwargs):
    order = instance.order
    order.amount = order.get_amount()
    order.save()
