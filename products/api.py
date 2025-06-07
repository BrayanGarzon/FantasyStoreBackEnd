from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status, generics
from rest_framework.exceptions import NotFound
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import CategoryProductModel, ProductModel, ReleasesProductModel
from .serializers import CategoryProductRequestSerializer, CategoryProductResponseSerializer, ProductResponseSerializer, \
    ProductRequestSerializer, ReleasesProductResponseSerializer, ProductsReleasesResponseSerializer


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


@extend_schema(tags=['Products'])
class ProductReleasesApiView(APIView):

    queryset = ReleasesProductModel.objects.all()

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    @extend_schema(tags=['Products'], responses={200: ProductsReleasesResponseSerializer})
    def get(self, request, *args, **kwargs):
        release_id = self.kwargs.get('release_id')

        try:
            release = ReleasesProductModel.objects.get(id=release_id)
        except ReleasesProductModel.DoesNotExist:
            raise NotFound("El lanzamiento no existe")

        products = release.products.all()
        serializer = ProductsReleasesResponseSerializer({
            'products': products,
            'releases': release,
        })
        return Response(serializer.data)


@extend_schema(tags=["Releases"])
class ReleasesProductsApiView(ModelViewSet):
    queryset = ReleasesProductModel.objects.all()
    serializer_class = ReleasesProductResponseSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]


@extend_schema(tags=["Releases"])
class ReleasesProductsLastReleaseApiView(GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ReleasesProductResponseSerializer


    @extend_schema(tags=["Releases"], responses={200: ReleasesProductResponseSerializer})
    def get(self, request, *args, **kwargs):
        try:
            release = ReleasesProductModel.objects.filter(priority=1).first()
            if not release:
                release = ReleasesProductModel.objects.order_by('-id').first()

            if not release:
                raise NotFound("No release found.")

            serializer = self.get_serializer(release)
            return Response(serializer.data)
        except NotFound as e:
            raise NotFound("No release found.")
        except Exception as e:
            raise e
