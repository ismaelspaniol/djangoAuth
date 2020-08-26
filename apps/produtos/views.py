from django.http import Http404
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Produto
from .serializers import ProdutoSerializer
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny
from utils.pagination import StandardResultsSetPagination, LargeResultsSetPagination


class ProdutosView(viewsets.ModelViewSet):
    pagination_class = LargeResultsSetPagination

    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    # http: // sulino.megakontroll.com: 8080 / produtos?descricao = milho
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('tenant', 'descricao')
    http_method_names = ['get', 'post', 'patch', 'delete']

    # metodo put tenque informar o objeto completo ja o metodo patch,
    # posso informar apenas um campo do objeto no json

    def get_queryset(self):
        return self.queryset.filter(tenant=self.request.tenant)
        # if self.request.method == "GET":
        #     content = {'user_count': '2'}
        # return HttpResponse(json.dumps(content), content_type='application/json')

    # def create(self, request, *args, **kwargs):
    #     serializer = ProdutoSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save(tenant_id=self.request.user.tenant.id)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    # def update(self, request, pk=None ):
    #     serializer = ProdutoSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.update(self.get_object(), serializer)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    # def destroy(self, request, pk=None):
    #     try:
    #         instance = self.get_object()
    #         self.perform_destroy(instance)
    #         content = {'status':'pk '+str(pk)+' deleted'}
    #     except Http404:
    #         content = {'error': 'not deleted'}
    #         Response(content, status=status.HTTP_400_BAD_REQUEST)
    #     return Response(content,status=status.HTTP_204_NO_CONTENT)



