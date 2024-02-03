# Generated by Django 3.1.5 on 2023-01-29 18:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('asteroid', '0007_itemtablemedia'),
    ]

    operations = [
        migrations.CreateModel(
            name='PartidoComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comm', models.TextField()),
                ('comm_partido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asteroid.partido')),
            ],
        ),
    ]