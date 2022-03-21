import string
import random

from django.utils import timezone
from django.db import models
from account.models import User


class Config(models.Model):
    weight = models.DecimalField(null=True, blank=True, max_digits=100000, decimal_places=2, default=3.05)
    cost = models.DecimalField(null=True, blank=True, max_digits=1000, decimal_places=2, default=1)

    def __str__(self):
        return f'{self.weight} Kg by {self.cost} Birr.'


class Carousel(models.Model):
    title = models.CharField(max_length=40, null=True, blank=True, default="")
    caption = models.CharField(max_length=150, null=True, blank=True, default="")
    photo = models.ImageField(upload_to='carousel')

    def __str__(self):
        return f'{self.title}'


class Feedback(models.Model):
    class Meta:
        ordering = ('date',)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=21)
    email = models.EmailField()
    subject = models.CharField(max_length=30, blank=True, null=True)
    body = models.TextField(max_length=200)
    date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name + "'s Comment"


class Post(models.Model):
    class Meta:
        ordering = ('date_send',)
        unique_together = ('track_id',)
    ran = ''.join(random.sample(string.ascii_letters + string.digits, k=5))

    postman = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="postman",)
    track_id = models.CharField(max_length=10, blank=True, default=ran)
    date_send = models.DateTimeField(auto_now_add=True, null=True)
    date_modified = models.DateTimeField(auto_now=True)

    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="sender")
    receiver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="receiver")
    sender_full_name = models.CharField(max_length=50, blank=True, null=True)
    sender_phone = models.CharField(max_length=50, blank=True, null=True)
    sender_address = models.CharField(max_length=50, blank=True, null=True)

    rec_full_name = models.CharField(max_length=50, blank=True, null=True)
    rec_phone = models.CharField(max_length=50, blank=True, null=True)
    post_box_num = models.CharField(max_length=50, null=True)
    rec_address = models.CharField(max_length=50, blank=True, null=True)
    post_location = models.CharField(max_length=50, null=True)
    seen = models.BooleanField(default=False)

    def is_sender_member(self):
        return False if self.sender is None else True

    def is_receiver_member(self):
        return False if self.receiver is None else True

    def __str__(self):
        if self.is_sender_member():
            return self.sender.first_name.title()
        else:
            return "User name is None" if self.sender_full_name is None else self.sender_full_name.title()

