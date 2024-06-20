from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    calories = models.CharField(max_length=35)
    fats = models.CharField(max_length=35)
    carbs = models.CharField(max_length=35)
    proteins = models.CharField(max_length=35)
    unsaturated_fats = models.CharField(max_length=35)
    sugar = models.CharField(max_length=35)
    salts = models.CharField(max_length=35)
    portion = models.CharField(max_length=35)

    def __str__(self):
        return self.title
