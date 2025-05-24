from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import Settings, Image, ImageTypeModel, ColorModel, SizeModel, ContactModel
from .serializers import SettingsSerializer, \
    ImageSerializerRequest, ImageTypeSerializer, CarouselItemResponseSerializer, CarouselItemRequestSerializer, \
    ColorRequestSerializer, ColorResponseSerializer, SizeRequestSerializer, SizeResponseSerializer, \
    ContactRequestSerializer, ContactResponseSerializer
from rest_framework.decorators import action
from .models import State, City, CarouselItemModel, ProductDistributionModel
from .serializers import StateSerializer, CitySerializer, StateWithCitiesSerializer, DistributionResponseSerializer, DistributionRequestSerializer



@extend_schema(tags=['Settings'])
class ConfigurationView(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = Settings.objects.all()
    serializer_class = SettingsSerializer


@extend_schema(tags=['Contact'])
class ContactApiView(ModelViewSet):
    queryset = ContactModel.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = ContactResponseSerializer

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ContactRequestSerializer
        return ContactResponseSerializer


@extend_schema(tags=["main"])
class PingView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response({"status": "ok"})


class StateViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = State.objects.all().order_by('id')
    serializer_class = StateSerializer

    def retrieve(self, request, *args, **kwargs):
        return Response(
            {"detail": "Method Not Allowed"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(detail=False, methods=['get'])
    def with_cities(self, request, *args, **kwargs):
        permission_classes = [permissions.AllowAny]
        states = State.objects.prefetch_related('cities').all()
        serializer = StateWithCitiesSerializer(states, many=True)
        return Response(serializer.data)


class CityViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = City.objects.all().order_by('id')
    serializer_class = CitySerializer

    def retrieve(self, request, *args, **kwargs):
        return Response(
            {"detail": "Method Not Allowed"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED)


@extend_schema(tags=['Image Type'])
class ImageTypeApiView(ModelViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = ImageTypeSerializer
    queryset = ImageTypeModel.objects.all()


@extend_schema(tags=['Images'])
class ImageApiView(generics.ListCreateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Image.objects.all()
    serializer_class = ImageSerializerRequest

    @extend_schema(
        request={
            'multipart/form-data': {
                'type': 'object',
                'properties': {
                    'image': {
                        'type': 'string',
                        'format': 'binary'
                    },
                    'type': {
                        'type': 'integer',
                    }
                }
            }
        },
        methods=["post"]
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


@extend_schema(tags=['Carousel'])
class CarouselApiView(ModelViewSet):
    queryset = CarouselItemModel.objects.all()
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CarouselItemRequestSerializer
        return CarouselItemResponseSerializer


@extend_schema(tags=['Product Distribution'])
class DistributionApiView(ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = ProductDistributionModel.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return DistributionRequestSerializer
        return DistributionResponseSerializer

@extend_schema(tags=['Products Colors'])
class ColorApiView(ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = ColorModel.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ColorRequestSerializer
        return ColorResponseSerializer


@extend_schema(tags=['Products Sizes'])
class SizeApiview(ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = SizeModel.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return SizeRequestSerializer
        return SizeResponseSerializer