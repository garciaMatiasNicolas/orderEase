from django.db import models
from users.models import Users
from store.models import Store


def upload_to(instance, filename):
    return f'product_images/{instance.created_by}{instance.name}/{filename}'


class Categories(models.Model):
    category_name = models.CharField(max_length=200)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.category_name


class Product(models.Model):
    product_name = models.CharField(max_length=250)
    price = models.IntegerField()
    stock = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(Users, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_to, blank=True, null=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)

    def __str__(self):
        return self.product_name

