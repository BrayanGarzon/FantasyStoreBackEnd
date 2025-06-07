from rest_framework import serializers

from main.models import Image
from main.serializers import ImageSerializer, ColorResponseSerializer, SizeResponseSerializer
from .models import  CategoryProductModel, ProductDistributionModel, ProductModel, ReleasesProductModel


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

class ProductDistributionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDistributionModel
        fields = ['color', 'size', 'stock', 'active', 'images']


class ProductDistributionResponseSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    color = ColorResponseSerializer(read_only=True)
    size = SizeResponseSerializer(read_only=True)

    class Meta:
        model = ProductDistributionModel
        fields = ['id', 'color', 'size', 'stock', 'active', 'images']


class ProductRequestSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=CategoryProductModel.objects.all())
    distributions = serializers.PrimaryKeyRelatedField(queryset=ProductDistributionModel.objects.all(), many=True)

    class Meta:
        model = ProductModel
        fields = ['name', 'description', 'stock', 'is_active', 'image', 'category', 'distributions', 'price', 'care', 'details']


class ProductResponseSerializer(serializers.ModelSerializer):
    category = CategoryProductResponseSerializer(read_only=True)
    distributions = ProductDistributionResponseSerializer(many=True, read_only=True)
    image = ImageSerializer(read_only=True)

    class Meta:
        model = ProductModel
        fields = ['id', 'name', 'description', 'stock', 'is_active', 'image', 'category', 'distributions', 'price', 'care', 'details']


class ReleasesProductResponseSerializer(serializers.ModelSerializer):
    image = ImageSerializer(read_only=True)

    class Meta:
        model = ReleasesProductModel
        fields = ('id', 'name', 'description', 'subtitle', 'sub_description', 'image',)


class ProductsReleasesResponseSerializer(serializers.Serializer):
    products = ProductResponseSerializer(many=True, read_only=True)
    releases = ReleasesProductResponseSerializer(read_only=True)