from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Denuncia
from .forms import DenunciaForm, LimitedDenunciaForm
from django.views.generic import TemplateView
from django.shortcuts import render
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import csv
from django.views.generic import View
from django.db.models import Q
from django.http import HttpResponse
import folium
from folium.plugins import HeatMap



class ExportarDenunciasCSV(View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="denuncias.csv"'

        writer = csv.writer(response)
        writer.writerow(['ID', 'Fecha', 'Tipo de Delito', 'Descripción', 'Estado'])

        denuncias = Denuncia.objects.all()

        for denuncia in denuncias:
            writer.writerow([denuncia.id, denuncia.fecha, denuncia.tipo_delito, denuncia.descripcion, denuncia.estado])

        return response


def estadisticas_denuncias(request):
    # Supongamos que obtienes los tipos de delito y la cantidad por tipo
    tipos_delito = ['Mano Armada', 'Fraude', 'Violencia','Secuestro','Extorcion']  # Aquí deberías tener tus tipos de delito como una lista de strings
    cantidad_por_tipo = [32, 20, 15, 40, 30]  # Aquí deberías tener la cantidad por tipo como una lista de números

    # Gráfico de Barras
    plt.figure(figsize=(10, 5))
    plt.bar(tipos_delito, cantidad_por_tipo, color='blue')
    plt.xlabel('Tipos de Delito')
    plt.ylabel('Cantidad')
    plt.title('Estadísticas de Denuncias por Tipo de Delito')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Guarda la figura en un buffer de bytes
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    # Codifica la imagen en base64 para incrustarla en HTML
    image_bar = buffer.getvalue()
    buffer.close()
    graphic_bar = base64.b64encode(image_bar).decode('utf-8')

    # Gráfico de Torta
    plt.figure(figsize=(8, 8))
    plt.pie(cantidad_por_tipo, labels=tipos_delito, autopct='%1.1f%%', startangle=140)
    plt.title('Distribución de Denuncias por Tipo de Delito')
    plt.tight_layout()

    # Guarda la figura en un buffer de bytes
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    # Codifica la imagen en base64 para incrustarla en HTML
    image_pie = buffer.getvalue()
    buffer.close()
    graphic_pie = base64.b64encode(image_pie).decode('utf-8')

    # Mapa de Calor
    m = folium.Map(location=[-34.6083, -58.3712], zoom_start=12)  # Ajusta la ubicación inicial y el zoom según tu necesidad

    # Coordenadas de zonas calientes
    heat_data = [
        [-34.5883, -58.4306],  # Palermo
        [-34.6091, -58.4005],  # Balvanera
        [-34.6346, -58.4360],  # Parque Chacabuco
        [-34.6289, -58.3839],  # Constitución
        [-34.5747, -58.4422]   # Colegiales
    ]

    HeatMap(heat_data).add_to(m)
    map_html = m._repr_html_()

    # Renderiza el template con las imágenes del gráfico
    return render(request, 'estadisticas_denuncias.html', {
        'graphic_bar': graphic_bar,
        'graphic_pie': graphic_pie,
        'map_html': map_html
    })


class HomeView(TemplateView):
    template_name = 'home.html'


class DenunciaListView(LoginRequiredMixin, ListView):
    model = Denuncia
    template_name = 'denuncias/denuncia_list.html'
    context_object_name = 'denuncias'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(titulo__icontains=query) |
                Q(descripcion__icontains=query) |
                Q(nombre_demandante__icontains=query) |
                Q(dni_demandante__icontains=query) |
                Q(estado__icontains=query) |
                Q(tipo_delito__icontains=query) |
                Q(barrio__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_employee'] = self.request.user.groups.filter(name='Empleado').exists()
        return context


class DenunciaDetailView(DetailView):
    model = Denuncia
    template_name = 'denuncias/denuncia_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            if user.is_superuser:
                context['can_edit'] = True
                context['can_delete'] = True
            elif user.groups.filter(name='Empleado').exists():
                context['can_edit'] = True
                context['can_delete'] = False  # Ajustar según los permisos del empleado
            else:
                context['can_edit'] = False
                context['can_delete'] = False
        else:
            context['can_edit'] = False
            context['can_delete'] = False
        return context

# En DenunciaUpdateView
class DenunciaUpdateView(LoginRequiredMixin, UpdateView):
    model = Denuncia
    form_class = DenunciaForm
    template_name = 'denuncias/denuncia_form.html'
    success_url = reverse_lazy('denuncia_list')

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.groups.filter(name='Empleado').exists()

    def get_form_class(self):
        if self.request.user.groups.filter(name='Empleado').exists():
            return LimitedDenunciaForm  # Empleados usarán el formulario limitado
        else:
            return DenunciaForm  # Otros usuarios usarán el formulario completo

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_employee'] = self.request.user.groups.filter(name='Empleado').exists()
        return context
    
    
class DenunciaCreateView(LoginRequiredMixin, CreateView):
    model = Denuncia
    form_class = DenunciaForm
    template_name = 'denuncias/denuncia_form.html'
    success_url = reverse_lazy('denuncia_list')



class DenunciaDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Denuncia
    template_name = 'denuncias/denuncia_confirm_delete.html'
    success_url = reverse_lazy('denuncia_list')

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.groups.filter(name='Empleado').exists()