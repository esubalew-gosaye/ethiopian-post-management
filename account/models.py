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
    last_name = models.CharField(max_length=150)
    email = models.EmailField(max_length=150)
    password = models.CharField(max_length=150)
    sex = models.CharField(max_length=10, choices=GENDER)
    address = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=15)
    is_counter = models.BooleanField(blank=True, default=False)
    is_admin = models.BooleanField(blank=True, default=False)
    is_costumer = models.BooleanField(blank=True, default=False)
    is_postman = models.BooleanField(blank=True, default=False)

    def get_absolute_url(self):
        return f"/me/{self.id}/"

    def __str__(self):
        return self.first_name+" "+self.middle_name
