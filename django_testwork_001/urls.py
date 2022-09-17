from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from catalog.v1.views import ProductsViewSet, CategoryPropsViewSet

ROUTER_SETTINGS = {"trailing_slash": False}

router = DefaultRouter(**ROUTER_SETTINGS)

router.register('category_props', CategoryPropsViewSet, basename='category-props')
router.register('products', ProductsViewSet, basename='products')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls))

]

urlpatterns += [path('silk', include('silk.urls', namespace='silk'))]