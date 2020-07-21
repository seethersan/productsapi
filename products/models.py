from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator, ValidationError

def validate_value(value):
    if value <= 0 or value >= 99999.9:
        raise ValidationError("Invalid value")

def validate_stock(value):
    if value <= -1:
        raise ValidationError("Invalid stock value")

# Create your models here.
class Category(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100, validators=[MinLengthValidator(3, "Invalid category name"), MaxLengthValidator(55, "Invalid category name")])
    description = models.CharField(max_length=250, validators=[MinLengthValidator(3, "Invalid category description"), MaxLengthValidator(250, "Invalid category description")])

    def __str__(self):
        return self.name

class Brand(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100, validators=[MinLengthValidator(2, "Invalid brand name"), MaxLengthValidator(30, "Invalid brand name")])

    def __str__(self):
        return self.name

class Product(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100, validators=[MinLengthValidator(3, "Invalid product name"), MaxLengthValidator(55, "Invalid product name")])
    value = models.FloatField(validators=[validate_value])
    discount_value = models.FloatField()
    categories = models.ManyToManyField(Category)
    brands = models.ManyToManyField(Brand)
    stock = models.IntegerField(validators=[validate_stock])

    def __str__(self):
        return self.name

    def clean(self):
        if self.discount_value >= self.value:
            raise ValidationError({"discount_value": "Invalid discount value"})