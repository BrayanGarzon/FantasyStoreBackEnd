from django.contrib import admin
from .models import CategoryProductModel, ProductDistributionModel, ProductModel
# Register your models here.

@admin.register(CategoryProductModel)
class CategoryProductAdmin(admin.ModelAdmin):
    pass

@admin.register(ProductModel)
class ProductAdmin(admin.ModelAdmin):
    pass

@admin.register(ProductDistributionModel)
class ProductDistributionAdmin(admin.ModelAdmin):
    pass
