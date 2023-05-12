from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    slug = models.SlugField(db_index=True)
    title = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.title
      

class Menu(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)  
    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=1)
    featured = models.BooleanField(db_index=True)

    def __str__(self) -> str:
        return self.title

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menuitem = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    
    def __str__(self) -> str:
        return f'{self.user} has {self.quantity} quantity of {self.menuitem} in the cart'
    
    class Meta:
        unique_together = ('menuitem', 'user')

class Order(models.Model):
    OUT_FOR_DELIVERY = 0
    DELIVERED = 1
    
    status_choices = (
    (OUT_FOR_DELIVERY, 'Pending'),
    (DELIVERED, 'Done'),
)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=status_choices, default=0)
    products = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='menus')
    # crew = models.ForeignKey(User, on_delete=models.CASCADE)

    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    items = models.ForeignKey(Cart, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)

class Delivery(models.Model):
    crew = models.ForeignKey(User, on_delete=models.CASCADE)
    orders = models.ForeignKey(Order, on_delete=models.CASCADE)
    