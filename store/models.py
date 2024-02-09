from django.db import models
from users.models import Users


# Store model
class Store(models.Model):
    store_name = models.CharField(max_length=200, unique=True)
    user_owner = models.ForeignKey(Users, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.store_name


# Additional information about the store
class StoreInformation(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    city = models.CharField(max_length=50)
    street_address = models.CharField(max_length=50)
    street_number = models.IntegerField(max_length=50)
    category = models.CharField(max_length=200)
    cuit = models.IntegerField()
    store_phone = models.IntegerField()

