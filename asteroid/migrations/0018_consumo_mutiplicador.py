# Generated by Django 4.2.2 on 2023-08-29 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asteroid', '0017_consumo_formato_consumo_lan'),
    ]

    operations = [
        migrations.AddField(
            model_name='consumo',
            name='mutiplicador',
            field=models.IntegerField(default=1),
        ),
    ]