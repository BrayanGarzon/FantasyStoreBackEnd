from urllib.parse import urljoin

from django.conf import settings
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from .models import Settings, State, City, Image, UnitOfMeasurement, CarouselItemModel, ImageTypeModel, \
    ProductDistributionModel, SizeModel, ColorModel


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


class ColorRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColorModel
        fields = ['name', 'hex']


class ColorResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColorModel
        fields = '__all__'


class SizeRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SizeModel
        fields = ['name']


class SizeResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SizeModel
        fields = '__all__'


class DistributionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDistributionModel
        fields = ['color', 'size', 'stock', 'active']


class DistributionResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDistributionModel
        fields = '__all__'


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
