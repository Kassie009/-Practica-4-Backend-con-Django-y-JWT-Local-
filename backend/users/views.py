from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

# --- IMPORTACIONES PARA SWAGGER ---
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
# ----------------------------------

from .models import User
from .serializers import UserSerializer, UserCreateUpdateSerializer


# --- ESTE ES EL CAMBIO ---
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
# -------------------------
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