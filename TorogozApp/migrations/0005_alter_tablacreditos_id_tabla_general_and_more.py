# Generated by Django 5.0.4 on 2024-04-08 23:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TorogozApp', '0004_rename_tabla_general_tablacreditos_id_tabla_general_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tablacreditos',
            name='id_tabla_general',
            field=models.ForeignKey(db_column='id_tabla_general', on_delete=django.db.models.deletion.CASCADE, to='TorogozApp.tablabalancegeneral'),
        ),
        migrations.AlterField(
            model_name='tablarenovaciones',
            name='id_tabla_general',
            field=models.ForeignKey(db_column='id_tabla_general', on_delete=django.db.models.deletion.CASCADE, to='TorogozApp.tablabalancegeneral'),
        ),
    ]
