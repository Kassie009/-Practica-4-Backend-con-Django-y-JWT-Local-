from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Aquí le decimos a Swagger cómo debe pedir la autenticación
schema_view = get_schema_view(
    openapi.Info(
        title="API Gestión Académica",
        default_version='v1',
        description="API para gestión de usuarios y matrículas - Práctica DWI",
        contact=openapi.Contact(email="admin@test.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    # ESTO ES LO QUE ARREGLA EL PROBLEMA:
    authentication_classes=[], 
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('users.urls')),
    
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]