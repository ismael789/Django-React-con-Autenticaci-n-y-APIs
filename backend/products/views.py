from rest_framework import viewsets, generics, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter
from .models import Category, Product, User
from .serializers import CategorySerializer, ProductSerializer, UserSerializer, PersonalDataSerializer
from .services import calcular_precio_final


class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class PersonalDataView(generics.RetrieveAPIView):
    serializer_class = PersonalDataSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


@extend_schema(
    parameters=[OpenApiParameter(name='code', type=str, required=False, description='Codigo ISO de dos letras, por ejemplo MX')],
    responses=OpenApiResponse(description='Datos del pais obtenidos desde CountryInfoService'),
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def soap_country(request):
    """Consulta CountryInfoService por medio de Zeep y responde JSON."""
    import requests
    from zeep import Client
    from zeep.transports import Transport
    from zeep.helpers import serialize_object

    code = request.query_params.get('code', 'MX').upper()
    wsdl = 'http://webservices.oorsprong.org/websamples.countryinfo/CountryInfoService.wso?WSDL'
    try:
        session = requests.Session()
        session.trust_env = False
        result = Client(wsdl=wsdl, transport=Transport(session=session, timeout=20)).service.FullCountryInfo(sCountryISOCode=code)
        data = serialize_object(result)
        return Response({'source': 'CountryInfoService', 'code': code, 'data': data})
    except Exception as exc:
        return Response(
            {'detail': 'No fue posible consultar el servicio SOAP.', 'code': code, 'error': str(exc)},
            status=status.HTTP_502_BAD_GATEWAY,
        )


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
