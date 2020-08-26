from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from apps.produtos import views
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

router = routers.DefaultRouter()
router.register(r'produtos', views.ProdutosView)

urlpatterns = [
    path('', include(router.urls)),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    path('token-refresh/', refresh_jwt_token),
    path('token-verify/', verify_jwt_token),
    path('token-auth/', obtain_jwt_token), #PARA OBTER O TOKEN,  NO HEADER USAR Authorization  JWT <TOKEN>
]
