from django import forms
from .models import Overhead, Product, RawMaterial, PackagingMaterial, RawMaterialQuantity, PackagingMaterialQuantity

class OverheadForm(forms.ModelForm):
    class Meta:
        model = Overhead
        fields = ['name', 'price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'custom-input'}),
            'price': forms.NumberInput(attrs={'class': 'custom-input'}),
        }

from django import forms
from .models import Product, RawMaterial, PackagingMaterial

class ProductSelectionForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Product.objects.all(), empty_label=None)



class ProductDataForm(forms.Form):
    def __init__(self, *args, product=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.product = product

        raw_materials = RawMaterial.objects.all()
        packaging_materials = PackagingMaterial.objects.all()

        for material in raw_materials:
            quantity_field_name = f'{material.name}_quantity'
            unit_price_field_name = f'{material.name}_unit_price'

            self.fields[quantity_field_name] = forms.DecimalField(
                label=f'{material.name} Quantity', required=False
            )
            self.fields[unit_price_field_name] = forms.DecimalField(
                label=f'{material.name} Unit Price', required=False
            )

        for material in packaging_materials:
            quantity_field_name = f'{material.name}_quantity'
            unit_price_field_name = f'{material.name}_unit_price'

            self.fields[quantity_field_name] = forms.DecimalField(
                label=f'{material.name} Quantity', required=False
            )
            self.fields[unit_price_field_name] = forms.DecimalField(
                label=f'{material.name} Unit Price', required=False
            )

        # Add the new fields for overhead_percentage, batches_per_month, items_in_batch, and markup
        self.fields['overhead_percentage'] = forms.DecimalField(
            label='Overhead Percentage', required=False
        )
        self.fields['batches_per_month'] = forms.IntegerField(
            label='Batches per Month', min_value=0, required=False
        )
        self.fields['items_in_batch'] = forms.IntegerField(
            label='Items in Batch', min_value=0, required=False
        )
        self.fields['markup'] = forms.DecimalField(
            label='Markup', required=False
        )



""" 
class AddProductForm(forms.Form):
    name = forms.CharField(label='Product Name')
    overhead_percentage = forms.DecimalField(label='Overhead Percentage', required=False)
    batches_per_month = forms.IntegerField(label='Batches per Month', min_value=0, required=False)
    items_in_batch = forms.IntegerField(label='Items in Batch', min_value=0, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        raw_materials = RawMaterial.objects.all()
        packaging_materials = PackagingMaterial.objects.all()

        for material in raw_materials:
            self.fields[f'{material.name}_quantity'] = forms.DecimalField(
                label=f'{material.name} Quantity', required=False
            )
            self.fields[f'{material.name}_unit_price'] = forms.DecimalField(
                label=f'{material.name} Unit Price', required=False
            )

        for material in packaging_materials:
            self.fields[f'{material.name}_quantity'] = forms.DecimalField(
                label=f'{material.name} Quantity', required=False
            )
            self.fields[f'{material.name}_unit_price'] = forms.DecimalField(
                label=f'{material.name} Unit Price', required=False
            )
            """)                                            this is the models.py (from django.db import models

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
