from rest_framework import serializers
from apps.user.models import MyUser
from rest_framework_jwt.settings import api_settings
from apps.tenants.serializer import TenantSerializer


class UserSerializer(serializers.ModelSerializer):
    requestTenant = serializers.SerializerMethodField()

    def get_requestTenant(self, obj):
        request = self._context.get("request")
        if request and hasattr(request, "tenant"):
            return TenantSerializer(request.tenant).data
        return None

    class Meta:
        model = MyUser
        fields = ('username', 'tenant', 'requestTenant', 'email', 'first_name', 'is_active', 'user_permissions',)






class UserSerializerWithToken(serializers.ModelSerializer):

    token = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    def get_token(self, obj):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        return token

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    class Meta:
        model = MyUser
        fields = ('token', 'username', 'password')