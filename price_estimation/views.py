from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404

from .forms import OverheadForm, ProductSelectionForm, ProductDataForm, AddProductForm

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

def enter_product_data(request, product_id):
    product = Product.objects.get(pk=product_id)
    raw_materials = RawMaterialQuantity.objects.filter(product=product)
    packaging_materials = PackagingMaterialQuantity.objects.filter(product=product)

    RawMaterialQuantityFormSet = modelformset_factory(
        RawMaterialQuantity,
        form=ProductDataForm,  # Use the appropriate form class here
        fields=('quantity', 'unit_price'),
        extra=0,
    )

    if request.method == 'POST':
        form = ProductDataForm(request.POST, product=product)
        formset = RawMaterialQuantityFormSet(request.POST, queryset=raw_materials)
        
        if form.is_valid() and formset.is_valid():
            # Process and save data
            product.overhead_percentage = form.cleaned_data['overhead_percentage']
            product.batches_per_month = form.cleaned_data['batches_per_month']
            product.items_in_batch = form.cleaned_data['items_in_batch']
            product.save()

            # Save RawMaterialQuantity formset
            formset.save()

            # Save PackagingMaterialQuantity formset similarly
            
            return redirect('select_product')

    else:
        initial_data = {
            'overhead_percentage': product.overhead_percentage,
            'batches_per_month': product.batches_per_month,
            'items_in_batch': product.items_in_batch,
        }
   
        form = ProductDataForm(initial=initial_data)  # Use the appropriate form class here
        formset = RawMaterialQuantityFormSet(queryset=raw_materials)

    context = {
        'product': product,
        'raw_materials': raw_materials,
        'packaging_materials': packaging_materials,
        'form': form,
        'formset': formset,  # Pass the formset to the context
    }
    return render(request, 'enter_product_data.html', context)




from django.shortcuts import render, redirect
from .forms import AddProductForm
from .models import RawMaterial, PackagingMaterial, Product

def add_product_data(request):
    if request.method == 'POST':
        form = AddProductForm(request.POST)
        if form.is_valid():
            # Process and save data
            product = Product.objects.create(
                name=form.cleaned_data['name'],
                overhead_percentage=form.cleaned_data['overhead_percentage'],
                batches_per_month=form.cleaned_data['batches_per_month'],
                items_in_batch=form.cleaned_data['items_in_batch']
            )

            raw_materials = RawMaterial.objects.all()
            packaging_materials = PackagingMaterial.objects.all()

            for material in raw_materials:
                quantity_field_name = f'{material.name}_quantity'
                unit_price_field_name = f'{material.name}_unit_price'
                quantity = form.cleaned_data.get(quantity_field_name)
                unit_price = form.cleaned_data.get(unit_price_field_name)
                if quantity is not None and unit_price is not None:
                    RawMaterialQuantity.objects.create(product=product, material=material, quantity=quantity, unit_price=unit_price)

            for material in packaging_materials:
                quantity_field_name = f'{material.name}_quantity'
                unit_price_field_name = f'{material.name}_unit_price'
                quantity = form.cleaned_data.get(quantity_field_name)
                unit_price = form.cleaned_data.get(unit_price_field_name)
                if quantity is not None and unit_price is not None:
                    PackagingMaterialQuantity.objects.create(product=product, material=material, quantity=quantity, unit_price=unit_price)

            return redirect('select_product')  # Redirect to a different page if needed
    else:
        form = AddProductForm()

    context = {
        'form': form,
    }
    return render(request, 'add_product_data.html', context)



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

        #overhead_cost = (total_material_cost * product.overhead_percentage) / 100
        overhead_percentage_used = total_overhead_price *(product.overhead_percentage/100) 

        estimated_batch_price = total_material_cost + (overhead_percentage_used / product.batches_per_month)
        estimated_item_price = estimated_batch_price / product.items_in_batch

        summaries.append({
            'product': product,
            'total_material_cost': total_material_cost,
            'overhead_percentage_used': overhead_percentage_used,
            'estimated_batch_price': estimated_batch_price,
            'estimated_item_price': estimated_item_price,
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

#def submit_product(request):
    #if request.method == 'POST':
        #form = ProductForm(request.POST)
        #if form.is_valid():
           # form.save()  # Save the form data to the database
           # return redirect('landing_page')  # Redirect back to the landing page or another relevant view
   # else:
#form = ProductForm()
    
    #return render(request, 'submit_product.html', {'form': form})


#def submit_raw_material(request):
    #if request.method == 'POST':
        #form = RawMaterialQuantityForm (request.POST)
        #if form.is_valid():
            #form.save()  # Save the form data to the database
            #return redirect('landing_page')  # Redirect back to the landing page or another relevant view
    #else:
        #form = RawMaterialQuantityForm()
    
    #return render(request, 'submit_raw_material.html', {'form': form})

#def submit_packaging_material(request):
    #if request.method == 'POST':
        #form = PackagingMaterialQuantityForm(request.POST)
        #if form.is_valid():
            #form.save()  # Save the form data to the database
            #return redirect('landing_page')  # Redirect back to the landing page or another relevant view
    #else:
        #form = PackagingMaterialQuantityForm()
    
    #return render(request, 'submit_packaging_material.html', {'form': form})

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