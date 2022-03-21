import random
import string

from django.db import models

# Create your models here.


class User(models.Model):
    GENDER = (
        ('F', "Female"),
        ('M', 'Male'),
        ('O', 'Other')
    )
    first_name = models.CharField(max_length=150)
    middle_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(max_length=150)
    password = models.CharField(max_length=150)
    sex = models.CharField(max_length=10, choices=GENDER)
    address = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=15)
    is_counter = models.BooleanField(blank=True, default=False)
    is_admin = models.BooleanField(blank=True, default=False)
    is_costumer = models.BooleanField(blank=True, default=False)
    is_postman = models.BooleanField(blank=True, default=False)
    is_manager = models.BooleanField(blank=True, default=False)

    def get_absolute_url(self):
        return f"/me/{self.id}/"

    def __str__(self):
        return self.first_name+" "+self.middle_name


class Revoke(models.Model):
    ran = ''.join(random.sample(string.ascii_letters + string.digits, k=5))
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=15, blank=True, default=f'POST:{ran}')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.first_name+" "+self.user.middle_name

