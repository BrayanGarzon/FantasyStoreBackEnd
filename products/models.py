from django.db import models
from main.models import Image
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