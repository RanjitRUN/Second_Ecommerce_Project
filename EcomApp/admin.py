from django.contrib import admin
from .models import Product,Customer,OrderPlaced, cart


@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name','locality', 'city', 'state', 'zipcode' ]


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'selling_price', 'discounted_price', 'description', 'brand', 'category', 'product_image']



@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'customer', 'quantity', 'ordered_date', 'status']

@admin.register(cart)
class cartModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity']