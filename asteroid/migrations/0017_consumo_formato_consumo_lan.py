# Generated by Django 4.2.2 on 2023-08-29 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asteroid', '0016_relitempersona'),
    ]

    operations = [
        migrations.AddField(
            model_name='consumo',
            name='formato',
            field=models.CharField(default='ND', max_length=128),
        ),
        migrations.AddField(
            model_name='consumo',
            name='lan',
            field=models.CharField(default='ND', max_length=2),
        ),
    ]