from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password


# Serializer para LEER datos (NUNCA incluye password)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'matricula', 'is_active', 'is_staff'
        ]
        # NOTA: 'password' NO está aquí. Esto corrige el error de seguridad
        # del manual donde la contraseña se devolvía en las respuestas.


# Serializer para CREAR y ACTUALIZAR (aquí SÍ se maneja la contraseña)
class UserCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'matricula', 'password', 'is_active', 'is_staff'
        ]
        extra_kwargs = {
            # write_only: la contraseña se puede enviar pero NUNCA se devuelve
            'password': {'write_only': True, 'required': False}
        }

    def create(self, validated_data):
        # Encriptar contraseña al crear
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # CORRECCIÓN: Solo actualizar contraseña si viene en la petición
        # El manual tenía un bug: si no enviabas password, sobrescribía
        # la contraseña del usuario con la del que hacía la petición.
        if 'password' in validated_data and validated_data['password']:
            validated_data['password'] = make_password(validated_data['password'])
        else:
            # Si no viene password, lo quitamos para que no se sobreescriba
            validated_data.pop('password', None)

        return super().update(instance, validated_data)