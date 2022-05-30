# Generated by Django 4.0.1 on 2022-05-29 19:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fornecedor', '0013_alter_fornecedor_id'),
        ('contas_a_pagar', '0004_alter_contas_pagar_options_alter_contas_pagar_table'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contas_pagar',
            name='Fornecedor',
        ),
        migrations.AddField(
            model_name='contas_pagar',
            name='Fornecedor',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='fornecedor.fornecedor'),
            preserve_default=False,
        ),
    ]