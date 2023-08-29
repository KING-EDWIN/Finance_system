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

        # Add the new fields for overhead_percentage, batches_per_month, and items_in_batch
        self.fields['overhead_percentage'] = forms.DecimalField(
            label='Overhead Percentage', required=False
        )
        self.fields['batches_per_month'] = forms.IntegerField(
            label='Batches per Month', min_value=0, required=False
        )
        self.fields['items_in_batch'] = forms.IntegerField(
            label='Items in Batch', min_value=0, required=False
        )



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