from django.urls import path
from . import views

urlpatterns = [
    path('', views.DenunciaListView.as_view(), name='denuncia_list'),
    
    path('new/', views.DenunciaCreateView.as_view(), name='denuncia_create'),
    path('<int:pk>/', views.DenunciaDetailView.as_view(), name='denuncia_detail'),
    path('denuncias/<int:pk>/update/', views.DenunciaUpdateView.as_view(), name='denuncia_update'),
    path('<int:pk>/delete/', views.DenunciaDeleteView.as_view(), name='denuncia_delete'),
    path('exportar-denuncias-csv/', views.ExportarDenunciasCSV.as_view(), name='exportar_denuncias_csv'),
    path('estadisticas/', views.estadisticas_denuncias, name='estadisticas_denuncias'),
]
