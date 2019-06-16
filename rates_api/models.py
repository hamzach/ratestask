from django.db import models
from django.utils.text import slugify

from .constants import DAY_CHOICES


class Region(models.Model):
    name = models.TextField()
    slug = models.SlugField()
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = slugify(self.name)
        super(Region, self).save(force_insert, force_update, using, update_fields)


class Port(models.Model):
    # 5-character Port Code
    code = models.CharField(max_length=5)
    name = models.TextField()
    region = models.ForeignKey(Region, on_delete=models.CASCADE)


class Price(models.Model):
    origin = models.ForeignKey(Port, on_delete=models.CASCADE, related_name='price_origin')
    destination = models.ForeignKey(Port, on_delete=models.CASCADE, related_name='price_destination')
    day = models.IntegerField(choices=DAY_CHOICES)
    price = models.DecimalField(decimal_places=2, max_digits=20)  # price is stored in USD
