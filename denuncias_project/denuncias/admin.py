# En denuncias/admin.py

from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Denuncia


from django.contrib import admin
from .models import Denuncia

@admin.register(Denuncia)
class DenunciaAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha', 'tipo_delito', 'estado')  # Ajusta esto según tus necesidades
    search_fields = ('id', 'tipo_delito', 'estado')  # Campos de búsqueda
    list_filter = ('estado', 'tipo_delito')  # Filtros laterales
    readonly_fields = ('fecha',)  # Campos solo de lectura

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser or request.user.groups.filter(name='Empleado').exists():
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False
