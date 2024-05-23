from django.contrib import admin
from .models import SaldoTotal, TablaBalanceGeneral,TablaCreditos,TablaRenovaciones,TablaRutas
admin.site.register(SaldoTotal),
admin.site.register(TablaBalanceGeneral),
admin.site.register(TablaCreditos),
admin.site.register(TablaRenovaciones),
admin.site.register(TablaRutas)
# Register your models here.
