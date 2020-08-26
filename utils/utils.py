from apps.user.serializer import UserSerializer
from apps.user.models import MyUser

def my_jwt_response_handler(token, user=None, request=None):
    print(user)
    a = request.tenant
    queryset = MyUser.objects.filter(pk = user.id, username=user.username, tenant=a )

    return {
        'token': token,
        'user': UserSerializer(queryset, context={'request': request}, many=True).data
    }