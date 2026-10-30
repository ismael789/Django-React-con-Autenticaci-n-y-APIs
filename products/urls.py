from django.urls import path, include
from .views import CategoryViewSet, ProductViewSet, UserViewSet, precio_final
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('products', ProductViewSet, basename='products')
router.register('categories', CategoryViewSet, basename='categories')
router.register('usuarios', UserViewSet, basename='usuarios')

urlpatterns = [
    path('products/<int:pk>/precio-final/', precio_final, name='precio_final'),
    path('', include(router.urls))
]
