from django import forms
from .models import (
    Overhead, Product, RawMaterial, PackagingMaterial, 
    RawMaterialQuantity, PackagingMaterialQuantity
)

# Overhead Form
class OverheadForm(forms.ModelForm):
    class Meta:
        model = Overhead
        fields = ['name', 'price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'custom-input'}),
            'price': forms.NumberInput(attrs={'class': 'custom-input'}),
        }

# Product Selection Form
class ProductSelectionForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Product.objects.all(), empty_label=None)

# Product Data Form
class ProductDataForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['overhead_percentage', 'batches_per_month', 'items_in_batch', 'markup']
        widgets = {
            'overhead_percentage': forms.NumberInput(attrs={'placeholder': 'Enter overhead %'}),
            'batches_per_month': forms.NumberInput(attrs={'placeholder': 'Enter batches per month'}),
            'items_in_batch': forms.NumberInput(attrs={'placeholder': 'Enter items in batch'}),
            'markup': forms.NumberInput(attrs={'placeholder': 'Enter markup %'}),
        }

    def __init__(self, *args, product=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.product = product


# Form for Raw Material Quantity
class RawMaterialQuantityForm(forms.ModelForm):
    class Meta:
        model = RawMaterialQuantity
        fields = ['id' ,'quantity', 'unit_price']  # The fields to be filled in the form

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['quantity'] = forms.DecimalField(
            label='Quantity', required=True
        )
        self.fields['unit_price'] = forms.DecimalField(
            label='Unit Price', required=True
        )

# Form for Packaging Material Quantity
class PackagingMaterialQuantityForm(forms.ModelForm):
    class Meta:
        model = PackagingMaterialQuantity
        fields = ['id', 'quantity', 'unit_price']  # The fields to be filled in the form

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['quantity'] = forms.DecimalField(
            label='Quantity', required=True
        )
        self.fields['unit_price'] = forms.DecimalField(
            label='Unit Price', required=True
        )

# Add Product Form (Commented out as you mentioned it was not needed currently)
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
"""
