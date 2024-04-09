from django.db import models

class SaldoTotal(models.Model):
    id_saldo_total = models.AutoField(primary_key=True)
    saldo_totalcol = models.FloatField()

    def str(self):
        return str(self.id_saldo_total)

class TablaBalanceGeneral(models.Model):
    id_registro = models.AutoField(primary_key=True)
    fecha = models.DateField()
    tipo = models.CharField(max_length=45)
    concepto = models.CharField(max_length=100)
    inversion = models.FloatField(null=True)
    ingresos_a_caja = models.FloatField(null=True)
    prestamo = models.FloatField(null=True)
    cobros = models.FloatField(null=True)
    creditos = models.FloatField(null=True)
    renovaciones = models.FloatField(null=True)
    salarios = models.FloatField(null=True)
    prestamos_trabajadores = models.FloatField(null=True)
    salidas = models.FloatField(null=True)
    total = models.FloatField(null=True)

    def str(self):
        return str(self.id_registro)

class TablaCreditos(models.Model):
    id_creditos = models.AutoField(primary_key=True)
    fecha = models.DateField(null=True)
    id_tabla_general = models.ForeignKey(TablaBalanceGeneral, on_delete=models.CASCADE, db_column='id_tabla_general')
    tipo_credito = models.CharField(max_length=45, null=True)
    cantidad = models.FloatField(null=True)

    def str(self):
        return str(self.id_creditos)

class TablaRenovaciones(models.Model):
    id_renovaciones = models.AutoField(primary_key=True)
    fecha = models.DateField(null=True)
    id_tabla_general = models.ForeignKey(TablaBalanceGeneral, on_delete=models.CASCADE, db_column='id_tabla_general')
    tipo_renovacion = models.CharField(max_length=45, null=True)
    cantidad = models.IntegerField(null=True)

    def str(self):
        return str(self.id_renovaciones)

class TablaRutas(models.Model):
    id_tabla_rutas = models.AutoField(primary_key=True)
    fecha = models.DateField(null=True)
    nombre_trabajador = models.CharField(max_length=45, null=True)
    tipo_ruta = models.CharField(max_length=45, null=True)
    cantidad = models.FloatField(null=True)

    def str(self):
        return str(self.id_tabla_rutas)

