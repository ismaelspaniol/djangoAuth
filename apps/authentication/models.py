from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class TestBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, tenant=None, **kwargs):
        UserModel = get_user_model()
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        try:
            user = UserModel.objects.get(username=username) # user name é unico username sempre composto por tenant.username
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user