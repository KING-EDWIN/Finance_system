"""
URL configuration for clari6 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from price_estimation  import views

urlpatterns = [

    path('', views.landing_page, name='landing_page'),

    path('admin/', admin.site.urls),
    path('', include("price_estimation.urls")),

    # URL to manage overheads
    path('manage_overheads/', views.manage_overheads, name='manage_overheads'),
    
    # URL to manage products
    # URL to manage a specific product
     path('select_product/', views.select_product, name='select_product'),
     path('enter_product_data/<int:product_id>/', views.enter_product_data, name='enter_product_data'),
     path('add_new_product/', views.add_product_data, name='add_product_data'),

    
    # URL to view product summary
    path('product_summaries/', views.product_summaries, name='product_summaries'),
    
    # URL to handle form submissions for overheads
    path('submit_overhead/', views.submit_overhead, name='submit_overhead'),
    
    # URL to handle form submissions for products
    #path('submit_product/', views.submit_product, name='submit_product'),
    
    # URL to handle form submissions for raw material quantities
    #path('submit_raw_material/<int:product_id>/<int:material_id>/', views.submit_raw_material, name='submit_raw_material'),
    
    # URL to handle form submissions for packaging material quantities
    #path('submit_packaging_material/<int:product_id>/<int:material_id>/', views.submit_packaging_material, name='submit_packaging_material'),

     path('edit_overhead/<int:overhead_id>/', views.edit_overhead, name='edit_overhead'),

     path('delete_overhead/<int:overhead_id>/', views.delete_overhead, name='delete_overhead'),

]
