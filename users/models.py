from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


# User Manager
class UserManager(BaseUserManager):
    def create_user(self, email: str, first_name: str, last_name: str, password: str = None) -> object:
        if not email:
            raise ValueError('User must have an email')

        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name
        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email: str, first_name: str, last_name: str,
                         password: str = None) -> object:
        admin = self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password
        )

        admin.is_admin = True
        admin.save()
        return admin


class UserInformation(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dni = models.IntegerField()
    phone = models.IntegerField()


# User model
class Users(AbstractUser):
    email = models.EmailField(max_length=200, unique=True)
    is_admin = models.BooleanField(default=False)
    account_is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user_information = models.OneToOneField(UserInformation, on_delete=models.CASCADE, null=True, blank=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name', 'last_name')

    def has_perm(self, perm, obj=None) -> bool:
        return True

    def has_module_perms(self, app_label) -> bool:
        return True

    @property
    def is_staff(self) -> object:
        return self.is_admin

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'

