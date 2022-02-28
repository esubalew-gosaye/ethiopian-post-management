from django.db import models


class Config(models.Model):
    distance = models.DecimalField(null=True, blank=True, max_digits=100000, decimal_places=2, default=3.05)
    cost = models.DecimalField(null=True, blank=True, max_digits=1000, decimal_places=2, default=1)

    def __str__(self):
        return f'{self.distance} Km by {self.cost} Birr.'


class Carousel(models.Model):
    title = models.CharField(max_length=40, null=True, blank=True, default="")
    caption = models.CharField(max_length=150, null=True, blank=True, default="")
    photo = models.ImageField(upload_to='carousel')

    def __str__(self):
        return f'{self.title}'
