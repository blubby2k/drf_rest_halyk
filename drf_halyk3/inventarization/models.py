from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, surname, role, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, surname=surname, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, surname, role, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, name, surname, role, password, **extra_fields)

class Category(models.Model):
    CATEGORY_CHOICES = [
        ('E', 'Electronic'),
        ('F', 'Furniture'),
        ('O', 'Other')
    ]
    name = models.CharField(max_length=255, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.name

class Items(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    current_location = models.CharField(max_length=255)
    expected_location = models.CharField(max_length=255)
    expected_time = models.DateTimeField()
    description = models.TextField()
    sender_name = models.CharField(max_length=100)
    recipient_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    created_by = models.ForeignKey('Employee', related_name='created_items', on_delete=models.SET_NULL, null=True)
    processed_by = models.ForeignKey('Employee', related_name='processed_items', on_delete=models.SET_NULL, null=True)

class Employee(AbstractBaseUser):
    first_name = models.CharField(max_length=255)
    second_name = models.CharField(max_length=255)
    role = models.CharField(max_length=100)
    access = models.CharField(max_length=100)
    login = models.CharField(max_length=50, unique=True)

    items = CustomUserManager()

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['email', 'first_name', 'second_name', 'role', 'access']

    def __str__(self):
        return f"{self.first_name} {self.second_name}"