from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse

# --- IMPORTACIONES PARA SWAGGER ---
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
# ----------------------------------

# --- IMPORTACIONES PARA SOAP ---
from zeep import Client
from zeep.transports import Transport
from requests import Session
# -------------------------------

from .models import User
from .serializers import UserSerializer, UserCreateUpdateSerializer


# --- ESTE ES EL CRUD DE USUARIOS ---
@swagger_auto_schema(
    manual_parameters=[
        openapi.Parameter(
            'Authorization', 
            openapi.IN_HEADER, 
            description="Token JWT. Escribe: Bearer <tu_token>", 
            type=openapi.TYPE_STRING,
            required=True
        )
    ]
)
class UserApiViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return UserCreateUpdateSerializer
        return UserSerializer


class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


# --- VISTA DEL SERVICIO SOAP ---
def soap_view(request):
    try:
        # Creamos una sesión de requests
        session = Session()
        session.verify = False # Ignorar SSL por pruebas locales
        
        # Creamos un transporte con timeout
        transport = Transport(session=session, timeout=15)
        
        # Consumimos el servicio SOAP de la calculadora
        client = Client(
            'http://www.dneonline.com/calculator.asmx?WSDL',
            transport=transport
        )
        
        # Sumamos 123 + 456
        result = client.service.Add(123, 456)
        
        return JsonResponse({
            'status': 'success',
            'operacion': '123 + 456',
            'resultado_soap': result
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)