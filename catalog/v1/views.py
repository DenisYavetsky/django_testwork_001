from rest_framework import mixins, viewsets

from catalog.models import Product, Category
from catalog.v1.serializers import ProductCreateSerializer, ProductListSerializer, ProductReadSerializer, \
    PropsSerializer


class CategoryPropsViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = PropsSerializer

    def get_queryset(self):
        if self.request.query_params.get('category'):
            return Category.objects.filter(id=self.request.query_params.get('category'))
        return Category.objects.all()


class ProductsViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Product.objects.all()

    def get_queryset(self):
        if self.request.query_params.get('category'):
            return Product.objects.filter(category=self.request.query_params.get('category'))
        return Product.objects.all()

    def get_serializer_class(self):

        serializers = {
            'create': ProductCreateSerializer,
            'retrieve': ProductReadSerializer,
            'list': ProductListSerializer
        }

        return serializers.get(self.action)

