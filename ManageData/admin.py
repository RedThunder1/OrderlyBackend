from django.contrib import admin

from .models import StoreModel, ProductModel


@admin.register(StoreModel)
class StoreAdmin(admin.ModelAdmin):
    list_display = ("UUID", "Name", "Address")
    search_fields = ("UUID", "Name", "Address")
    list_filter = ("Address",)
    ordering = ("Name",)


@admin.register(ProductModel)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "store", "price", "is_available")
    search_fields = ("name", "store__Name")
    list_filter = ("is_available", "store")
    ordering = ("store", "name")

# Register your models here.
