from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Produto


class ProdutoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Produto
        fields = '__all__'