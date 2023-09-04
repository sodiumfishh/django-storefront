from django.db import models

class Collection(models.Model):
  title = models.CharField(max_length=255)

class Product(models.Model):
  title = models.CharField(max_length=255)
  description = models.TextField()
  collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
  price = models.DecimalField(max_digits=6, decimal_places=2)
  inventory = models.IntegerField()
  last_update = models.DateTimeField(auto_now=True)

class Customer(models.Model):
  MEMBERSHIP_BRONZE = 'B'
  MEMBERSHIP_GOLD = 'G'
  MEMBERSHIP_SILVER = 'S'

  MEMBERSHIP_CHOICES = [
    (MEMBERSHIP_BRONZE, 'Bronze'),
    (MEMBERSHIP_SILVER, 'Silver'),
    (MEMBERSHIP_GOLD, 'Gold'),
  ]

  first_name = models.CharField(max_length=255)
  last_name = models.CharField(max_length=255)
  email = models.EmailField(unique=True)
  phone = models.CharField(max_length=255)
  birth_date = models.DateField(null=True)
  membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)

class Order(models.Model):
  PAYMENT_STATUS_PENDING = 'P'
  PAYMENT_STATUS_COMPLETED = 'C'
  PAYMENT_STATUS_FAILED = 'F'

  PAYMENT_STATUS_CHOICES = [
    (PAYMENT_STATUS_PENDING, 'Pending'),
    (PAYMENT_STATUS_COMPLETED, 'Completed'),
    (PAYMENT_STATUS_FAILED, 'Failed'),
  ]

  placed_at = models.DateTimeField(auto_now=True)
  payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
  customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

class OrderItem(models.Model):
  order = models.ForeignKey(Order, on_delete=models.CASCADE)
  product = models.ForeignKey(Product, on_delete=models.PROTECT)
  quantity = models.PositiveSmallIntegerField()
  unit_price = models.DecimalField(max_digits=6, decimal_places=2)

class Address(models.Model):
  street = models.CharField(max_length=255)
  city = models.CharField(max_length=255)
  # the cusomer field is a primary key to prevent duplicates, i.e., one customer cannot create many address objects
  # customer = models.OneToOneField(Customer, on_delete=models.CASCADE, primary_key=True)

  customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

class Cart(models.Model):
  customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
  updated_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
  cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  quantity = models.PositiveSmallIntegerField()