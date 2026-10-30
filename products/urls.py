from django.urls import path, include
from .views import CategoryViewSet, ProductViewSet, UserViewSet, RegisterUserView, PersonalDataView, precio_final, soap_country
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('products', ProductViewSet, basename='products')
router.register('categories', CategoryViewSet, basename='categories')
router.register('usuarios', UserViewSet, basename='usuarios')

urlpatterns = [
    path('auth/register/', RegisterUserView.as_view(), name='register'),
    path('auth/me/', PersonalDataView.as_view(), name='auth-me'),
    path('soap/country/', soap_country, name='soap-country'),
    path('products/<int:pk>/precio-final/', precio_final, name='precio_final'),
    path('', include(router.urls))
]
