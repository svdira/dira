# Generated by Django 4.0.6 on 2023-05-06 19:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('asteroid', '0011_consumo_season'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=256)),
                ('texto', models.TextField()),
                ('item_note', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asteroid.item')),
            ],
        ),
    ]
