# Generated by Django 4.1.5 on 2023-09-08 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asteroid', '0018_consumo_mutiplicador'),
    ]

    operations = [
        migrations.AddField(
            model_name='contrato',
            name='number',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='contrato',
            name='position',
            field=models.CharField(default='Not Specified', max_length=256),
        ),
        migrations.AddField(
            model_name='jugador',
            name='biographics',
            field=models.TextField(default='This section needs to be expanded.'),
        ),
    ]
