from django.db import models
from django.utils.text import slugify


class Region(models.Model):
    name = models.CharField(max_length=75)
    slug = models.CharField(max_length=75, unique=True)
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class Port(models.Model):
    # 5-character Port Code
    code = models.CharField(max_length=5, unique=True)
    name = models.CharField(max_length=75)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {}'.format(self.name, self.code)


class Price(models.Model):
    origin = models.ForeignKey(Port, on_delete=models.CASCADE, related_name='price_origin')
    destination = models.ForeignKey(Port, on_delete=models.CASCADE, related_name='price_destination')
    day = models.DateField()
    price = models.DecimalField(decimal_places=2, max_digits=20)  # price is stored in USD
