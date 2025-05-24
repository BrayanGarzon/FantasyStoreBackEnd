from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import CategoryProductModel, ProductModel
from .serializers import CategoryProductRequestSerializer, CategoryProductResponseSerializer, ProductResponseSerializer, ProductRequestSerializer


@extend_schema(tags=['Categories'])
class CategoriesApiView(ModelViewSet):
    queryset = CategoryProductModel.objects.all()
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CategoryProductRequestSerializer
        return CategoryProductResponseSerializer

    @extend_schema(
        responses={201: CategoryProductResponseSerializer},
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        serializer_response = CategoryProductResponseSerializer(serializer.instance)
        headers = self.get_success_headers(serializer_response.data)
        return Response(serializer_response.data, status=status.HTTP_201_CREATED, headers=headers)


@extend_schema(tags=['Products'])
class ProductsApiView(ModelViewSet):
    queryset = ProductModel.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = ProductResponseSerializer

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ProductRequestSerializer
        return ProductResponseSerializer

    @extend_schema(
        request={
            'multipart/form-data': {
                'type': 'object',
                'properties': {
                    'name': {
                        'type': 'string',

                    },
                    'description': {
                        'type': 'string',
                    },
                    'stock': {
                        'type': 'integer',
                    },
                    'is_active': {
                        'type': 'boolean',
                    },
                    'category': {
                        'type': 'integer',
                    },
                    'distribution': {
                        'type': 'integer',
                    },
                    'image': {
                        'type': 'string',
                        'format': 'binary'
                    }
                }
            }
        },
        responses={201: ProductResponseSerializer},
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        serializer_response = ProductResponseSerializer(serializer.instance)
        headers = self.get_success_headers(serializer_response.data)
        return Response(serializer_response.data, status=status.HTTP_201_CREATED, headers=headers)
