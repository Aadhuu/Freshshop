from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='categories/')
    description=models.TextField()
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='products/')
    description = models.TextField()
    price = models.IntegerField()
    stock = models.IntegerField()
    available = models.BooleanField(default=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name='products')
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)


