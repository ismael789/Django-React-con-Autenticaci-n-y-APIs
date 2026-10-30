from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiResponse
from .models import Category, Product, User
from .serializers import CategorySerializer, ProductSerializer, UserSerializer, PersonalDataSerializer
from .services import calcular_precio_final


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category']


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer

    def get_permissions(self):
        # El registro inicial debe ser posible antes de obtener el primer JWT.
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['get'], url_path='datos-personales')
    def datos_personales(self, request):
        return Response(PersonalDataSerializer(request.user).data)


@extend_schema(
    responses=OpenApiResponse(description='Precio final calculado con descuento')
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def precio_final(request, pk):
    """Facade que obtiene el producto y calcula su precio con descuento."""
    return Response(calcular_precio_final(pk))
