from django.contrib import admin
from .models import Overhead, RawMaterial, PackagingMaterial, Product, RawMaterialQuantity, PackagingMaterialQuantity

class RawMaterialQuantityInline(admin.TabularInline):
    model = RawMaterialQuantity
    extra = 1

class PackagingMaterialQuantityInline(admin.TabularInline):
    model = PackagingMaterialQuantity
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [RawMaterialQuantityInline, PackagingMaterialQuantityInline]
    list_display = ['name', 'overhead_percentage', 'batches_per_month' , 'items_in_batch' ]
    list_filter = ['overhead_percentage', 'batches_per_month', 'items_in_batch']
    search_fields = ['name']

@admin.register(Overhead)
class OverheadAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']
    search_fields = ['name']

@admin.register(RawMaterial, PackagingMaterial)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(RawMaterialQuantity, PackagingMaterialQuantity)
class MaterialQuantityAdmin(admin.ModelAdmin):
    list_display = ['product', 'material', 'quantity', 'unit_price']
    list_filter = ['product', 'material']
    search_fields = ['product__name', 'material__name']



