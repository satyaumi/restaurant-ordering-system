from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=50)
    slug =models.SlugField(unique=True)
    class Meta:
        verbose_name_plural ='Category'

    def __str__(self):
        return self.category_name

class Item(models.Model):
    item_name =models.CharField(max_length=40)
    description=models.TextField()
    price =models.FloatField()
    category =models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)
    image =models.ImageField(upload_to='items/')

    class Meta:
        verbose_name_plural ='Items'

    def __str__(self):
        return self.item_name
    

class AboutUs(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    class Meta:
        verbose_name_plural ='AboutUS'

    def __str__(self):
        return self.title

   
    
class Feedback(models.Model):
    user_name =models.CharField(max_length=30)
    description =models.TextField()
    rating =models.IntegerField()
    selfie =models.ImageField(upload_to='feedback/',blank=True)
    
    class Meta:
        verbose_name_plural ='Feedback'
    def __str__(self):
        return self.user_name

class BookTable(models.Model):
    name =models.CharField(max_length=15)
    phone_number =models.CharField(max_length=10)
    email =models.EmailField()
    total_person =models.IntegerField()
    booking_date =models.DateField(auto_now=False, auto_now_add=False)
    
    class Meta:
        verbose_name_plural ='BookTable'
    def __str__(self):
        return self.name

class Cart(models.Model):
    user =models.ForeignKey(User,related_name='cart',on_delete=models.CASCADE)
    item =models.ForeignKey(Item,related_name='cart_items',on_delete=models.CASCADE)
    quantity =models.PositiveIntegerField(default=1)
    
    discount_percent =models.PositiveIntegerField(default=0)
    def discounted_price(self):
        if self.discount_percent >0:
            return self.item.price *(100 -self.discount_percent)/100
        return self.item.price
    def total_price(self):
        return self.discounted_price() * self.quantity
    class Meta:
        verbose_name_plural ='Cart'
        unique_together =['user','item']
    
    def __str__(self):
        return f"{self.user.username} - {self.item.item_name}"
    


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.id}"



class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.FloatField()

    def __str__(self):
        return self.item.item_name
