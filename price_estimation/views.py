from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404

from .forms import OverheadForm, ProductSelectionForm, ProductDataForm

#from .forms import OverheadForm, PackagingMaterialQuantityForm, ProductForm, RawMaterialQuantityForm
from .models import Overhead, RawMaterial, PackagingMaterial, Product, RawMaterialQuantity, PackagingMaterialQuantity


from django.shortcuts import render

def landing_page(request):
    return render(request, 'landing_page.html')

from django.shortcuts import render, redirect

def manage_overheads(request):
    predefined_overheads = [
        'Salaries', 'Kitchen', 'Lab', 'Stationery', 'NSSF 10%',
        'Generator fuel', 'Umeme', 'Depreciation', 'Waste Collection and Disposal',
        'Environmental ( Pest monitoring & Control)', 'Security', 'Telephone & Internet',
        'Laundry', 'Staff Medical', 'Repairs and Maintenance', 'Legal', 'Car fuel',
        'Sewage and rubbish collection', 'NWSC', 'Marketing fees', 'Audit'
    ]

    overheads = Overhead.objects.all()

    if request.method == 'POST':
        overhead_name = request.POST.get('overhead_name')
        if overhead_name == 'new':
            overhead_name = request.POST.get('new_overhead', '')
        price = request.POST['price']
        Overhead.objects.create(name=overhead_name, price=price)
        return redirect('manage_overheads')

    overhead_names = [overhead.name for overhead in overheads]
    context = {'overhead_names': overhead_names, 'overheads': overheads, 'predefined_overheads': predefined_overheads}
    return render(request, 'manage_overheads.html', context)


def select_product(request):
    # Retrieve all existing products from the database
    products = Product.objects.all()

    if request.method == 'POST':
        # If the form has been submitted (a product has been selected)
        form = ProductSelectionForm(request.POST)
        if form.is_valid():
            # Get the selected product ID from the form data
            selected_product_id = form.cleaned_data['product']

            # Check if the user clicked on the "Add Product" button
            if 'add_product' in request.POST:
                # Redirect to the "Add Product Data" page
                return redirect('add_product_data')
            
            # Redirect to the "Enter Product Data" page for the selected product
            return redirect('enter_product_data', product_id=selected_product_id)
    else:
        # If the request method is GET (initial page load), create an empty form
        form = ProductSelectionForm()

    # Render the "Select Product" template with the form and the list of products
    return render(request, 'select_product.html', {'form': form, 'products': products})


from django.forms import modelformset_factory
from .forms import ProductDataForm  # Import the ProductDataForm

from django.forms import modelformset_factory
from .forms import ProductDataForm  # Import the ProductDataForm
from django.forms import modelformset_factory
from .forms import ProductDataForm, RawMaterialQuantityForm, PackagingMaterialQuantityForm  # Separate forms
from django.forms import modelformset_factory
from .forms import ProductDataForm, RawMaterialQuantityForm, PackagingMaterialQuantityForm  # Separate forms

def enter_product_data(request, product_id):
    product = Product.objects.get(pk=product_id)
    raw_materials = RawMaterialQuantity.objects.filter(product=product)
    packaging_materials = PackagingMaterialQuantity.objects.filter(product=product)

    RawMaterialQuantityFormSet = modelformset_factory(
        RawMaterialQuantity,
        form=RawMaterialQuantityForm,  # Separate form class for raw material
        extra=0,
    )

    PackagingMaterialQuantityFormSet = modelformset_factory(
        PackagingMaterialQuantity,
        form=PackagingMaterialQuantityForm,  # Separate form class for packaging material
        extra=0,
    )

    if request.method == 'POST':
        print("POST data:", request.POST) 
        product_form = ProductDataForm(request.POST, instance=product)
        raw_material_formset = RawMaterialQuantityFormSet(request.POST, queryset=raw_materials)
        packaging_material_formset = PackagingMaterialQuantityFormSet(request.POST, queryset=packaging_materials)

        if product_form.is_valid() and raw_material_formset.is_valid() and packaging_material_formset.is_valid():
            # Save product data
            updated_product = product_form.save(commit=False)
            updated_product.save()
            print(f"Product {product.name} updated successfully.")

            # Save RawMaterialQuantity formset
            raw_material_formset.save()
            print("Raw materials updated successfully.")

            # Save PackagingMaterialQuantity formset
            packaging_material_formset.save()
            print("Packaging materials updated successfully.")

            return redirect('select_product')
        else:
            print("Form errors:", product_form.errors, raw_material_formset.errors, packaging_material_formset.errors)
         
         # Re-fetch the material instances for each form in the formsets after errors
        raw_material_formset = RawMaterialQuantityFormSet(queryset=RawMaterialQuantity.objects.filter(product=product))
        packaging_material_formset = PackagingMaterialQuantityFormSet(queryset=PackagingMaterialQuantity.objects.filter(product=product))
            
    else:
        product_form = ProductDataForm(instance=product)
        raw_material_formset = RawMaterialQuantityFormSet(queryset=raw_materials)
        packaging_material_formset = PackagingMaterialQuantityFormSet(queryset=packaging_materials)

    context = {
        'product': product,
        'product_form': product_form,  # Product form
        'raw_material_formset': raw_material_formset,  # Raw materials formset
        'packaging_material_formset': packaging_material_formset,  # Packaging materials formset
    }
    return render(request, 'enter_product_data.html', context)





from django.shortcuts import render, redirect
#from .forms import AddProductForm
from .models import RawMaterial, PackagingMaterial, Product


def product_summaries(request):
    products = Product.objects.all()

    total_overhead_price = sum(overhead.price for overhead in Overhead.objects.all())
    
    summaries = []
    for product in products:
        raw_materials = RawMaterialQuantity.objects.filter(product=product)
        packaging_materials = PackagingMaterialQuantity.objects.filter(product=product)
        
        total_raw_cost = sum(material.quantity * material.unit_price for material in raw_materials)
        total_packaging_cost = sum(material.quantity * material.unit_price for material in packaging_materials)
        total_material_cost = total_raw_cost + total_packaging_cost

        overhead_percentage_used = total_overhead_price * (product.overhead_percentage / 100)

        estimated_batch_price = total_material_cost + (overhead_percentage_used / product.batches_per_month)
        estimated_item_price = estimated_batch_price / product.items_in_batch

        # Calculate the selling price using the provided markup
        if product.markup is not None:
            selling_price = (estimated_item_price * product.markup / 100) + estimated_item_price
        else:
            selling_price = None


        # Rounding to two decimal places
        total_material_cost = round(total_material_cost, 2)
        overhead_percentage_used = round(overhead_percentage_used, 2)
        estimated_batch_price = round(estimated_batch_price, 2)
        estimated_item_price = round(estimated_item_price, 2)
        total_raw_cost= round(total_raw_cost,2)
        total_packaging_cost=round(total_packaging_cost,2)
        selling_price=round(selling_price,2)



        summaries.append({
            'product': product,
            'total_raw_cost': total_raw_cost, 
            'total_packaging_cost': total_packaging_cost,
            'total_material_cost': total_material_cost,
            'overhead_percentage_used': overhead_percentage_used,
            'estimated_batch_price': estimated_batch_price,
            'estimated_item_price': estimated_item_price,
            'markup': product.markup,  # Include markup in the context
            'selling_price': selling_price,  # Include calculated selling price in the context
        })

    context = {'summaries': summaries}
    return render(request, 'product_summaries.html', context)


def submit_overhead(request):
    if request.method == 'POST':
        form = OverheadForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to the database
            return redirect('landing_page')  # Redirect back to the landing page or another relevant view
    else:
        form = OverheadForm()
    
    return render(request, 'submit_overhead.html', {'form': form})              

def edit_overhead(request, overhead_id):
    overhead = get_object_or_404(Overhead, id=overhead_id)

    if request.method == 'POST':
        form = OverheadForm(request.POST, instance=overhead)
        if form.is_valid():
            form.save()
            return redirect('manage_overheads')

    else:
        form = OverheadForm(instance=overhead)

    return render(request, 'edit_overhead.html', {'form': form})

def delete_overhead(request, overhead_id):
    overhead = get_object_or_404(Overhead, id=overhead_id)
    if request.method == 'POST':
        overhead.delete()
        return redirect('manage_overheads')
    return render(request, 'delete_overhead.html', {'overhead': overhead})  
