# Generated by Django 4.2.3 on 2024-06-14 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("asteroid", "0030_matchsquad_squadplayers"),
    ]

    operations = [
        migrations.AlterField(
            model_name="consumo",
            name="fecha_fin",
            field=models.DateField(blank=True, null=True),
        ),
    ]