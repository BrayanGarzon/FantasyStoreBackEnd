from django.contrib import admin

from .models import CategoryProductModel, ProductDistributionModel, ProductModel, ReleasesProductModel
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


@admin.register(ReleasesProductModel)
class ReleasesProductsLastReleaseApiView(admin.ModelAdmin):
    list_display = ('id', 'name', 'created', 'priority')
    search_fields = ('id', 'name')

    filter_horizontal = ('products',)