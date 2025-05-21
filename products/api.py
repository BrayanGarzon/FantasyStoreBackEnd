from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import CategoryProductModel
from .serializers import CategoryProductRequestSerializer, CategoryProductResponseSerializer


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