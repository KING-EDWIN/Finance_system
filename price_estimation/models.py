

from django.db import models

class Overhead(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return self.name

class RawMaterial(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class PackagingMaterial(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    overhead_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    batches_per_month = models.PositiveIntegerField()
    items_in_batch = models.PositiveIntegerField()
    markup = models.DecimalField(max_digits=5, decimal_places=2, default= 20)

    def __str__(self):
        return self.name


class RawMaterialQuantity(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    material = models.ForeignKey(RawMaterial, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} - {self.material.name}"

class PackagingMaterialQuantity(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    material = models.ForeignKey(PackagingMaterial, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} - {self.material.name}"
