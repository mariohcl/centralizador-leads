"""
URL configuration for centralizador_leads project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from leads import views as views
from django.contrib.auth import views as auth_views
from leads import views as lead_views
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from leads import views
from leads.views import resumen_general


def home_redirect_view(request):
    if request.user.is_authenticated:
        return redirect('ferias')
    return redirect('login')

urlpatterns = [
    path('admin/', admin.site.urls),

    # LOGIN/LOGOUT automático de Django
    path('accounts/', include('django.contrib.auth.urls')),

    # Home -> redirige al login
    path('', auth_views.LoginView.as_view(template_name='login.html'), name='login'),

    # Rutas protegidas
    path('', home_redirect_view, name='home'),
    path('ferias/', views.ferias_panel, name='ferias'),
    path('dashboard/<slug:feria_slug>/', login_required(lead_views.dashboard_feria), name='dashboard_feria'),
    path('dashboard/<slug:feria_slug>/exportar/', login_required(lead_views.exportar_excel_feria), name='exportar_excel_feria'),

    path('dashboard/<slug:feria_slug>/', views.dashboard_feria, name='dashboard_feria'),
    path('dashboard/<slug:feria_slug>/exportar/', views.exportar_excel_feria, name='exportar_excel_feria'),

    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path("feria/<str:feria_slug>/actualizar/", views.actualizar_leads, name="actualizar_leads"),
    path('resumen/', resumen_general, name='resumen_general'),

]
