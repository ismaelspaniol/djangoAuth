from django.db import models
from apps.tenants.models import TenantAwareModel


class Produto(TenantAwareModel):
    descricao = (models.CharField(max_length=10, blank=True))

    class Meta:
        db_table = 'produtos'

    def __str__(self):
        return self.tenant.name + ' | '+self.descricao

