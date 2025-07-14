from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('dashboard/', views.redireccion_dashboard, name='dashboard'),
    path('ferias/', views.ferias_panel, name='ferias'), # 👈 esta línea
    path('dashboard/<slug:feria_slug>/', views.dashboard_feria, name='dashboard_feria'),
    path('dashboard/<slug:feria_slug>/exportar/', views.exportar_excel_feria, name='exportar_excel_feria'),
    path('feria/<slug:feria_slug>/actualizar/', views.actualizar_leads, name='actualizar_leads'),
    path('resumen/', views.resumen_general, name='resumen_general'),
] 
