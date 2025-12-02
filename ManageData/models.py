from django.db import models
from django.db.models import CharField, TextField


# Create your models here.
class StoreModel(models.Model):
    UUID = models.CharField(max_length=255, blank=True, primary_key=True)
    Name = models.CharField(max_length=255, null=True)
    Description = models.TextField(null=True)
    Address = models.CharField(max_length=255, null=True)
    Items = models.TextField(null=True)
    # Maybe add an image for stores

    class Meta:
        db_table = 'stores'


    class Meta:
        db_table = 'stores'


class ProductModel(models.Model):
    store = models.ForeignKey(
        StoreModel,
        related_name="products",
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_available = models.BooleanField(default=True)
    image_url = models.URLField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.store.Name})"
    
class Cart(models.Model):
    user = models.ForeignKey(
        'UserAuth.UserAccount',
        on_delete=models.CASCADE,
        related_name='cart'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cart'
    
    def __str__(self):
        return f"{self.user.username}'s Cart"
    

class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        ProductModel,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = 'cart_items'

    def __str__(self):
        return f"{self.product.name} x{self.quantity}"

class Order(models.Model):
    user = models.ForeignKey(
        'UserAuth.UserAccount',
        on_delete=models.CASCADE,
        related_name='orders'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        db_table = 'orders'

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        ProductModel,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        db_table = 'order_items'

    def __str__(self):
        return f"{self.product.name} x{self.quantity}"

