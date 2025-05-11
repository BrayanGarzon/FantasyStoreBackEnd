from urllib.parse import urljoin

from django.conf import settings
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from .models import Settings, State, City, Product, Image, UnitOfMeasurement, CarouselItemModel, ImageTypeModel


class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settings
        fields = ['key', 'value']


class ImageTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageTypeModel
        fields = '__all__'



class ImageSerializerRequest(serializers.ModelSerializer):
    type = ImageTypeSerializer(read_only=True)

    class Meta:
        model = Image
        fields = ['id', 'image', 'type']


class ImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    type = ImageTypeSerializer(read_only=True)

    class Meta:
        model = Image
        fields = ['id', 'image', 'type']

    @extend_schema_field(OpenApiTypes.STR)
    def get_image(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri(obj.image.url)
            else:
                return urljoin(settings.BASE_URL, obj.image.url)
        return ''



class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ['id', 'name']


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name']


class StateWithCitiesSerializer(serializers.ModelSerializer):
    cities = CitySerializer(many=True, read_only=True)

    class Meta:
        model = State
        fields = ['id', 'name', 'cities']


class UnitOfMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitOfMeasurement
        fields = '__all__'


class GeneralMessageSerializer(serializers.Serializer):
    message = serializers.CharField()


class ProductServiceRequestSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )
    unit_of_measurement = serializers.PrimaryKeyRelatedField(queryset=UnitOfMeasurement.objects.all())

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'unit_of_measurement', 'units', 'images']

    def create(self, validated_data):
        # Extraer las imágenes del producto
        images_data = validated_data.pop('images', [])
        print(images_data)

        # Crear el producto
        product = Product.objects.create(**validated_data)

        # Asociar las imágenes al producto
        for image_data in images_data:
            image_instance = Image.objects.create(image=image_data)
            product.images.add(image_instance)

        return product


class ProductServiceResponseSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'unit_of_measurement', 'units', 'images']


class CarouselItemRequestSerializer(serializers.ModelSerializer):
    image = serializers.PrimaryKeyRelatedField(queryset=Image.objects.all())

    class Meta:
        model = CarouselItemModel
        fields = ['title', 'image', 'order']


class CarouselItemResponseSerializer(serializers.ModelSerializer):
    image = ImageSerializer(read_only=True)

    class Meta:
        model = CarouselItemModel
        fields = ['id', 'image', 'title']
        read_only_fields = ['id',]
