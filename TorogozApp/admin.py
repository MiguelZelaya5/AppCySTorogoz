from django.contrib import admin
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

from .models import TablaBalanceGeneral, TablaCreditos, TablaRenovaciones, TablaRutas

# Función para exportar los datos a PDF
def export_as_pdf(queryset, fields):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=Tabla.pdf'

    doc = SimpleDocTemplate(response, pagesize=landscape(letter))
    elements = []

    # Excluir campos específicos para TablaCreditos y TablaRenovaciones
    if 'id_tabla_general' in fields:
        fields.remove('id_tabla_general')

    data = [fields]

    for obj in queryset:
        data.append([str(getattr(obj, field)) for field in fields])

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(table)
    doc.build(elements)

    return response

# Administrador base para reutilizar campos y funciones comunes
class BaseAdmin(admin.ModelAdmin):
    actions = ['export_as_pdf']

# Admin para TablaBalanceGeneral
class TablaBalanceGeneralAdmin(BaseAdmin):
    search_fields = ['fecha', 'tipo', 'concepto']
    list_display = ['fecha', 'tipo', 'concepto', 'inversion', 'ingresos_a_caja', 'prestamo', 'cobros',
                    'creditos', 'renovaciones', 'salarios', 'prestamos_trabajadores', 'salidas', 'total']

    def export_as_pdf(self, request, queryset):
        fields = [field.name for field in self.model._meta.fields]
        return export_as_pdf(queryset, fields)

    export_as_pdf.short_description = "Exportar a PDF"

# Admin para TablaCreditos
class TablaCreditosAdmin(BaseAdmin):
    search_fields = ['fecha', 'tipo_credito']
    list_display = ['fecha', 'tipo_credito', 'cantidad']

    def export_as_pdf(self, request, queryset):
        fields = [field.name for field in self.model._meta.fields]
        return export_as_pdf(queryset, fields)

    export_as_pdf.short_description = "Exportar a PDF"

# Admin para TablaRenovaciones
class TablaRenovacionesAdmin(BaseAdmin):
    search_fields = ['fecha', 'tipo_renovacion']
    list_display = ['fecha', 'tipo_renovacion', 'cantidad']

    def export_as_pdf(self, request, queryset):
        fields = [field.name for field in self.model._meta.fields]
        return export_as_pdf(queryset, fields)

    export_as_pdf.short_description = "Exportar a PDF"

# Admin para TablaRutas
class TablaRutasAdmin(BaseAdmin):
    search_fields = ['fecha', 'tipo_ruta']
    list_display = ['fecha', 'tipo_ruta', 'cantidad']

    def export_as_pdf(self, request, queryset):
        fields = [field.name for field in self.model._meta.fields]
        return export_as_pdf(queryset, fields)

    export_as_pdf.short_description = "Exportar a PDF"

# Registrar los modelos y sus admins personalizados
admin.site.register(TablaBalanceGeneral, TablaBalanceGeneralAdmin)
admin.site.register(TablaCreditos, TablaCreditosAdmin)
admin.site.register(TablaRenovaciones, TablaRenovacionesAdmin)
admin.site.register(TablaRutas, TablaRutasAdmin)
