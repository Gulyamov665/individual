from django.contrib.auth.models import User
from django.db import models


class Product(models.Model):
    title = models.CharField('Заголовок', max_length=255, )
    description = models.TextField()
    slug = models.SlugField(null=True)
    price = models.IntegerField()
    is_new = models.BooleanField()
    is_discounted = models.BooleanField()
    category = models.ForeignKey('shop.Category', default=None, on_delete=models.CASCADE)
    brand = models.ForeignKey('shop.Brand', default=None, on_delete=models.CASCADE)
    thumb = models.ImageField(default='default.png', null=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'shop_products'
        verbose_name_plural = 'Продукт'
        verbose_name = 'Продукт'


class Category(models.Model):
    name = models.CharField(max_length=225)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'shop_categories'


class Brand(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'shop_brands'


class Slide(models.Model):
    image = models.ImageField(default='slide.jpg')


class CardItem(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return self.product.title

    def total_price(self):
        return self.product.price * self.quantity


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    phone = models.IntegerField()
    total_price = models.IntegerField()

    def __str__(self):
        return f'Order # {self.pk}'


class OrderProduct(models.Model):
    order = models.ForeignKey('shop.Order', on_delete=models.CASCADE, related_name='order_products')
    product = models.ForeignKey('shop.Product', on_delete=models.CASCADE)
    amount = models.CharField(max_length=255)
    total = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.product} x {self.amount} - {self.order.customer.username}'


RATE_CHOICES = [
    (1, '1 - Trash'),
    (2, '2 - Bad'),
    (3, '3 - OK'),
    (4, '4 - Good'),
    (5, '5 - Perfect'),
]


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    text = models.TextField(blank=True)
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES, null=True)

    def __str__(self):
        return self.user.username
