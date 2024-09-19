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



from django import forms
from .models import RawMaterial, PackagingMaterial

class ProductDataForm(forms.Form):
    def __init__(self, *args, product=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.product = product

        raw_materials = RawMaterial.objects.all()
        packaging_materials = PackagingMaterial.objects.all()

        # Dynamically add fields for raw materials
        for material in raw_materials:
            quantity_field_name = f'raw_material_{material.id}_quantity'
            unit_price_field_name = f'raw_material_{material.id}_unit_price'

            self.fields[quantity_field_name] = forms.DecimalField(
                label=f'{material.name} Quantity', required=False, decimal_places=2
            )
            self.fields[unit_price_field_name] = forms.DecimalField(
                label=f'{material.name} Unit Price', required=False, decimal_places=2
            )

        # Dynamically add fields for packaging materials
        for material in packaging_materials:
            quantity_field_name = f'packaging_material_{material.id}_quantity'
            unit_price_field_name = f'packaging_material_{material.id}_unit_price'

            self.fields[quantity_field_name] = forms.DecimalField(
                label=f'{material.name} Quantity', required=False, decimal_places=2
            )
            self.fields[unit_price_field_name] = forms.DecimalField(
                label=f'{material.name} Unit Price', required=False, decimal_places=2
            )

        # Add fields for product-specific data
        self.fields['overhead_percentage'] = forms.DecimalField(
            label='Overhead Percentage (%)', required=False, decimal_places=2
        )
        self.fields['batches_per_month'] = forms.IntegerField(
            label='Batches per Month', min_value=0, required=False
        )
        self.fields['items_in_batch'] = forms.IntegerField(
            label='Items in Batch', min_value=0, required=False
        )
        self.fields['markup'] = forms.DecimalField(
            label='Markup (%)', required=False, decimal_places=2
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
            """
