from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from leads import views as lead_views
from leads.views import resumen_general
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

def home_redirect_view(request):
    if request.user.is_authenticated:
        return redirect('ferias')
    return redirect('login')

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Login y logout personalizados
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # Recuperación de contraseña con templates personalizados
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),

    # Página inicial según autenticación
    path('', home_redirect_view, name='home'),

    # Rutas de la app
    path('ferias/', lead_views.ferias_panel, name='ferias'),
    path('dashboard/<slug:feria_slug>/', login_required(lead_views.dashboard_feria), name='dashboard_feria'),
    path('dashboard/<slug:feria_slug>/exportar/', login_required(lead_views.exportar_excel_feria), name='exportar_excel_feria'),
    path("feria/<str:feria_slug>/actualizar/", lead_views.actualizar_leads, name="actualizar_leads"),
    path('resumen/', resumen_general, name='resumen_general'),
]
