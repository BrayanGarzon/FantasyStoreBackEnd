from rest_framework import serializers

from main.models import Image
from main.serializers import ImageSerializer
from .models import CategoryProductModel


class CategoryProductRequestSerializer(serializers.ModelSerializer):
    image = serializers.PrimaryKeyRelatedField(queryset=Image.objects.all())

    class Meta:
        model = CategoryProductModel
        fields = ['name', 'description', 'image', 'is_active']

class CategoryProductResponseSerializer(serializers.ModelSerializer):
    image = ImageSerializer(read_only=True)

    class Meta:
        model = CategoryProductModel
        fields = ['id', 'name', 'description', 'image', 'is_active']