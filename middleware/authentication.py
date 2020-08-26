from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from rest_framework.status import (
    HTTP_404_NOT_FOUND
)

from apps.authentication.tokenAuthentication import JSONWebTokenAuthentication
from apps.tenants.models import Tenant
from apps.user.models import MyUser


class AuthenticationTenant(MiddlewareMixin):
    def process_request(self, request):
        tenant = tenant_from_request(request)
        if tenant:
            request.tenant = tenant
            jwt_authentication = JSONWebTokenAuthentication()
            if jwt_authentication.get_jwt_value(request):
                try:
                    username, jwt = jwt_authentication.authenticate_with_tenant(request)
                except Exception as e:
                    return JsonResponse({'error': {'message': str(e)}}, status=HTTP_404_NOT_FOUND)

                user = tenant_user_from_request(tenant.id, username)

                if not user:
                    return JsonResponse({'error': {'message': 'Invalid Tenant access'}},
                                        status=HTTP_404_NOT_FOUND)
                else:
                    request.user = user
                    request.tenant = tenant
        else:
            return JsonResponse({'error': {'message': 'Requested tenant is not available'}},
                                status=HTTP_404_NOT_FOUND)


def tenant_from_request(request):
    hostname = hostname_from_request(request)
    subdomain_prefix = hostname.split(".")[0]
    return Tenant.objects.filter(subdomain_prefix=subdomain_prefix).first()


def tenant_user_from_request(tenant_id, username):
    return MyUser.objects.filter(is_active=True, username=username, tenant__id=tenant_id).first()


def hostname_from_request(request):
    # split on `:` to remove port
    return request.get_host().split(":")[0].lower()