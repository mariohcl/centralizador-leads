from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Lead
import requests
import pandas as pd
from datetime import datetime
import openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows
from io import BytesIO
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import HttpResponse
from leads.ferias import FERIAS
from django.contrib import messages
from django.urls import reverse
from django.db.models import Count, Max
from django.utils.text import slugify
from leads.models import Lead
from django.template.loader import render_to_string
from django.conf import settings




@login_required
def ferias_panel(request):
    ferias = [
        {'slug': 'hyvolution', 'nombre': 'Hyvolution'},
        {'slug': 'seguridadexpo', 'nombre': 'SeguridadExpo'},
        {'slug': 'exponaval', 'nombre': 'Exponaval'},
        {'slug': 'transport', 'nombre': 'Transport'},
        {'slug': 'enloce', 'nombre': 'Enloce'},
        {'slug': 'exposalud', 'nombre': 'Exposalud'},
        {'slug': 'expovivienda', 'nombre': 'Expovivienda'},
        {'slug': 'aquasur', 'nombre': 'Aquasur'},
        {'slug': 'aquasurtech', 'nombre': 'Aquasurtech'},
        {'slug': 'expomin', 'nombre': 'Expomin'},
        # agrega las demás ferias aquí
    ]
    return render(request, 'ferias.html', {'ferias': ferias})


@login_required
def redireccion_dashboard(request):
    return redirect('ferias')  # o redireccionar a una feria por defecto




@login_required
def dashboard_feria(request, feria_slug):
    if feria_slug not in FERIAS:
        return HttpResponse("Feria no válida", status=404)

    endpoint = FERIAS[feria_slug]
    datos_por_idioma = {}

    for lang in ['es', 'en']:
        fuente = f"{feria_slug}_{lang}"
        leads = Lead.objects.filter(fuente=fuente)

        fecha_inicio = request.GET.get('fecha_inicio')
        fecha_fin = request.GET.get('fecha_fin')

        if fecha_inicio:
            leads = leads.filter(fecha_envio__date__gte=fecha_inicio)
        if fecha_fin:
            leads = leads.filter(fecha_envio__date__lte=fecha_fin)

        df_original = pd.DataFrame(list(leads.values()))
        df_unicos = df_original.drop_duplicates(subset=['email'])
        duplicados = len(df_original) - len(df_unicos)

        if df_unicos.empty:
            datos_por_idioma[lang] = {'resumen': [], 'suma_total': 0, 'duplicados': 0}
            continue

        df_unicos['fecha_envio'] = pd.to_datetime(df_unicos['fecha_envio'])
        df_unicos['año'] = df_unicos['fecha_envio'].dt.isocalendar().year
        df_unicos['n_semana'] = df_unicos['fecha_envio'].dt.isocalendar().week
        df_unicos['inicio_semana'] = df_unicos['fecha_envio'] - pd.to_timedelta(df_unicos['fecha_envio'].dt.weekday, unit='D')
        df_unicos['semana_etiqueta'] = df_unicos['inicio_semana'].dt.strftime("Semana %U (%d/%m/%Y)")

        resumen = (
            df_unicos.groupby(['año', 'n_semana', 'semana_etiqueta'])
            .size()
            .reset_index(name='total_leads')
            .sort_values(['año', 'n_semana'], ascending=False)
        )

        datos_por_idioma[lang] = {
            'resumen': resumen.to_dict(orient='records'),
            'suma_total': resumen['total_leads'].sum(),
            'duplicados': duplicados
        }

    return render(request, 'dashboard.html', {
        'feria': feria_slug,
        'logo': endpoint['logo'],
        'datos_es': datos_por_idioma.get('es'),
        'datos_en': datos_por_idioma.get('en')
    })




# --- EXPORTAR A EXCEL ---
@login_required
def exportar_excel_feria(request, feria_slug):
    lang = request.GET.get("lang", "es")  # por defecto: español

    if feria_slug not in FERIAS:
        return HttpResponse("Feria no válida", status=404)

    endpoint = FERIAS[feria_slug]
    cf7_ids = endpoint.get("cf7_ids", {})

    cf7_id = cf7_ids.get(lang)
    if not cf7_id:
        return HttpResponse("No hay datos disponibles para este idioma.", status=400)

    headers = {"Authorization": f"Bearer {endpoint['token']}"}

    try:
        response = requests.get(endpoint["url"], headers=headers)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        return HttpResponse(f"Error de conexión con la API: {e}", status=500)

    # Filtrar por el cf7_id correspondiente al idioma
    data = [item for item in data if str(item.get("cf7_id")) == str(cf7_id)]

    for item in data:
        envio_id = item["envio_id"]
        fecha_envio = item["fecha_envio"]
        campos = item["datos"]

        Lead.objects.update_or_create(
            envio_id=envio_id,
            fuente=f"{feria_slug.lower()}_{lang.lower()}",
            defaults={
                "fecha_envio": fecha_envio,
                "nombre": campos.get("your-name"),
                "apellido": campos.get("your-lastname"),
                "cargo": campos.get("your-position"),
                "empresa": campos.get("your-company"),
                "email": campos.get("your-email"),
                "telefono": campos.get("tel-588"),
                "pais": campos.get("your-country"),
                "ip": campos.get("submit_ip"),
            },
        )

    leads = Lead.objects.filter(fuente=f"{feria_slug}_{lang}")

    fecha_inicio = request.GET.get("fecha_inicio")
    fecha_fin = request.GET.get("fecha_fin")

    if fecha_inicio:
        leads = leads.filter(fecha_envio__date__gte=fecha_inicio)
    if fecha_fin:
        leads = leads.filter(fecha_envio__date__lte=fecha_fin)

    df_original = pd.DataFrame(list(leads.values()))
    conteo = df_original["email"].value_counts().to_dict()
    df_original["repeticiones"] = df_original["email"].map(conteo)

    df_unicos = df_original.drop_duplicates(subset="email", keep="first")
    df_unicos = df_unicos.sort_values(by="fecha_envio")

    if df_unicos.empty:
        return HttpResponse("No hay datos para exportar.", content_type="text/plain")

    df_unicos["fecha_envio"] = pd.to_datetime(df_unicos["fecha_envio"])
    df_unicos["fecha_envio"] = df_unicos["fecha_envio"].dt.tz_localize(None)
    df_unicos["año"] = df_unicos["fecha_envio"].dt.isocalendar().year
    df_unicos["n_semana"] = df_unicos["fecha_envio"].dt.isocalendar().week
    df_unicos["inicio_semana"] = df_unicos["fecha_envio"] - pd.to_timedelta(
        df_unicos["fecha_envio"].dt.weekday, unit="D"
    )
    df_unicos["semana_etiqueta"] = df_unicos["inicio_semana"].dt.strftime("Semana %U (%d/%m)")

    resumen = (
        df_unicos.groupby(["año", "n_semana", "semana_etiqueta"])
        .size()
        .reset_index(name="total_leads")
        .sort_values(["año", "n_semana"])
    )

    wb = openpyxl.Workbook()
    ws1 = wb.active
    ws1.title = "Leads únicos"
    for r in dataframe_to_rows(df_unicos, index=False, header=True):
        ws1.append(r)

    ws2 = wb.create_sheet("Resumen semanal")
    for r in dataframe_to_rows(resumen, index=False, header=True):
        ws2.append(r)

    output = BytesIO()
    wb.save(output)
    output.seek(0)

    response = HttpResponse(
        output.getvalue(),
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = f'attachment; filename=leads_{feria_slug}_{lang}.xlsx'
    return response


@login_required
def ferias_panel(request):
    ferias = [
        {'slug': 'hyvolution', 'nombre': 'Hyvolution Chile', 'logo': 'logos/hyvolution.png'},
        {'slug': 'seguridadexpo', 'nombre': 'SeguridadExpo', 'logo': 'logos/seguridadexpo.png'},
        {'slug': 'exponaval', 'nombre': 'Exponaval', 'logo': 'logos/exponaval.png'},
        {'slug': 'transport', 'nombre': 'Transport', 'logo': 'logos/transport.png'},
        {'slug': 'enloce', 'nombre': 'Enloce', 'logo': 'logos/enloce.png'},
        {'slug': 'exposalud', 'nombre': 'Exposalud', 'logo': 'logos/exposalud.png'},
        {'slug': 'expovivienda', 'nombre': 'Expovivienda', 'logo': 'logos/expovivienda.png'},
        {'slug': 'aquasur', 'nombre': 'Aquasur', 'logo': 'logos/aquasur.png'},
        {'slug': 'aquasurtech', 'nombre': 'Aquasurtech', 'logo': 'logos/aquasurtech.png'},
        {'slug': 'expomin', 'nombre': 'Expomin', 'logo': 'logos/expomin.png'},
        # ... continúa con las demás
    ]
    return render(request, 'ferias.html', {'ferias': ferias})

@login_required
def actualizar_leads(request, feria_slug):
    lang = request.GET.get("lang", "es")

    if feria_slug not in FERIAS:
        messages.error(request, "Feria no válida.")
        return redirect("dashboard_feria", feria_slug=feria_slug)

    endpoint = FERIAS[feria_slug]
    cf7_ids = endpoint.get("cf7_ids", {})
    cf7_id = cf7_ids.get(lang)

    if not cf7_id:
        messages.warning(request, f"No hay formulario para el idioma {lang.upper()}.")
        return redirect("dashboard_feria", feria_slug=feria_slug)

    headers = {"Authorization": f"Bearer {endpoint['token']}"}

    try:
        response = requests.get(endpoint["url"], headers=headers)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        messages.error(request, f"Error al conectar con la API: {e}")
        return redirect("dashboard_feria", feria_slug=feria_slug)

    data = [item for item in data if str(item.get("cf7_id")) == str(cf7_id)]

    for item in data:
        envio_id = item["envio_id"]
        fecha_envio = item["fecha_envio"]
        campos = item["datos"]

        Lead.objects.update_or_create(
            envio_id=envio_id,
            fuente=f"{feria_slug.lower()}_{lang.lower()}",
            defaults={
                "fecha_envio": fecha_envio,
                "nombre": campos.get("your-name"),
                "apellido": campos.get("your-lastname"),
                "cargo": campos.get("your-position"),
                "empresa": campos.get("your-company"),
                "email": campos.get("your-email"),
                "telefono": campos.get("tel-588"),
                "pais": campos.get("your-country"),
                "ip": campos.get("submit_ip"),
            },
        )

    messages.success(request, f"Leads actualizados correctamente ({lang.upper()}).")
    return redirect(f"{reverse('dashboard_feria', args=[feria_slug])}?lang={lang}")

@login_required
def resumen_general(request):
    resumen = []

    for slug, feria in FERIAS.items():
        for lang in feria.get('cf7_ids', {}).keys():  # es/en
            fuente = f"{slug}_{lang}"
            leads = Lead.objects.filter(fuente=fuente)

            total_exportados = leads.count()
            filtrados = leads.values('email').distinct().count()
            duplicados = total_exportados - filtrados
            ultima_fecha = leads.aggregate(Max('fecha_envio'))['fecha_envio__max']

            resumen.append({
                'fuente': f"{feria['nombre']} ({lang.upper()})",
                'total_exportados': total_exportados,
                'duplicados': duplicados,
                'filtrados': filtrados,
                'ultima_fecha': ultima_fecha.strftime("%d/%m/%Y %H:%M") if ultima_fecha else '—',
                'url': reverse('dashboard_feria', args=[slug]) + f"?lang={lang}",
                'excel_url': reverse('exportar_excel_feria', args=[slug]) + f"?lang={lang}"
            })

    return render(request, 'resumen_general.html', {'ferias': resumen})


