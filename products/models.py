from django.db import models
from main.models import Image, ProductDistributionModel
from django.utils.translation import gettext_lazy as _

# Create your models here.


class CategoryProductModel(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True)
    is_active = models.BooleanField(default=True)
    image = models.ForeignKey(Image, on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ProductModel(models.Model):
    name = models.CharField(_("Nombre del Producto"), max_length=255)
    description = models.TextField(_("Descripción del Producto"), null=True)
    stock = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    category = models.ForeignKey("CategoryProductModel", on_delete=models.CASCADE)
    distributions = models.ManyToManyField(ProductDistributionModel, related_name='products', blank=True)
    price = models.IntegerField(default=0)
    care = models.TextField(max_length=255, null=True)
    details = models.TextField(null=True)
    favorite = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Producto")
        verbose_name_plural = _("Productos")
        ordering = ("name",)


class ReleasesProductModel(models.Model):
    name = models.CharField(_("Nombre del Producto"), max_length=255)
    description = models.TextField(null=True)
    title = models.CharField(_("Titulo"), max_length=255)
    subtitle = models.CharField(_("Subtitle"), max_length=255)
    sub_description = models.TextField(null=True)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    priority = models.IntegerField(default=1)
    products = models.ManyToManyField(ProductModel, related_name='releases', blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = _("Lanzamientos")
        verbose_name = _("Lanzamiento")
        ordering = ['priority']