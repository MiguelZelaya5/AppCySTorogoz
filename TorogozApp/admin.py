from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.formats.base_formats import CSV, XLS, JSON, YAML, HTML
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from .models import SaldoTotal, TablaBalanceGeneral, TablaCreditos, TablaRenovaciones, TablaRutas

# Recursos de importación/exportación
class SaldoTotalResource(resources.ModelResource):
    class Meta:
        model = SaldoTotal

class TablabalancegeneralResource(resources.ModelResource):
    class Meta:
        model = TablaBalanceGeneral

class TablaCreditosResource(resources.ModelResource):
    class Meta:
        model = TablaCreditos

class TablaRenovacionesResource(resources.ModelResource):
    class Meta:
        model = TablaRenovaciones

class TablaRutasResource(resources.ModelResource):
    class Meta:
        model = TablaRutas

# Clase personalizada para exportar datos a PDF
class PDFExporter:
    def export_data(self, queryset, model_name):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{model_name}.pdf"'
        
        doc = SimpleDocTemplate(response, pagesize=landscape(letter))
        elements = []

        data = [[field.verbose_name for field in queryset.model._meta.fields]]

        for obj in queryset:
            row = [str(getattr(obj, field.name)) for field in queryset.model._meta.fields]
            data.append(row)

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

# Clase base para admin con import/export y PDF
class BaseAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    def export_as_pdf(self, request, queryset):
        model_name = queryset.model._meta.verbose_name_plural.replace(' ', '_')
        pdf_exporter = PDFExporter()
        return pdf_exporter.export_data(queryset, model_name)

    export_as_pdf.short_description = "Export Selected to PDF"
    actions = [export_as_pdf]

# Admin para SaldoTotal
class SaldoTotalAdmin(BaseAdmin):
    search_fields = ['saldo_totalcol']
    list_display = ['id_saldo_total', 'saldo_totalcol']
    resource_class = SaldoTotalResource

# Admin para TablaBalanceGeneral
class TablaBalanceGeneralAdmin(BaseAdmin):
    search_fields = ['fecha', 'tipo', 'concepto']
    list_display = ['fecha', 'tipo', 'concepto', 'inversion', 'ingresos_a_caja', 'prestamo', 'cobros', 
                    'creditos', 'renovaciones', 'salarios', 'prestamos_trabajadores', 'salidas', 'total']
    resource_class = TablabalancegeneralResource

# Admin para TablaCreditos
class TablaCreditosAdmin(BaseAdmin):
    search_fields = ['fecha', 'tipo_credito']
    list_display = ['fecha', 'tipo_credito', 'cantidad', 'id_tabla_general']
    resource_class = TablaCreditosResource

# Admin para TablaRenovaciones
class TablaRenovacionesAdmin(BaseAdmin):
    search_fields = ['fecha', 'tipo_renovacion']
    list_display = ['fecha', 'tipo_renovacion', 'cantidad', 'id_tabla_general']
    resource_class = TablaRenovacionesResource

# Admin para TablaRutas
class TablaRutasAdmin(BaseAdmin):
    search_fields = ['fecha', 'tipo_ruta']
    list_display = ['fecha', 'tipo_ruta', 'cantidad']
    resource_class = TablaRutasResource

# Registrar los modelos y sus admins personalizados
admin.site.register(SaldoTotal, SaldoTotalAdmin)
admin.site.register(TablaBalanceGeneral, TablaBalanceGeneralAdmin)
admin.site.register(TablaCreditos, TablaCreditosAdmin)
admin.site.register(TablaRenovaciones, TablaRenovacionesAdmin)
admin.site.register(TablaRutas, TablaRutasAdmin)
