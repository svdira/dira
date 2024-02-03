# Generated by Django 3.1.5 on 2022-06-20 00:41

import asteroid.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('asteroid', '0002_colitem_cuenta_trx_trxtyp'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contrato',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Equipo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=128)),
                ('pais', models.CharField(max_length=128)),
                ('logo', models.ImageField(blank=True, max_length=255, null=True, upload_to=asteroid.models.path_and_name)),
            ],
        ),
        migrations.CreateModel(
            name='Jugador',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=128)),
                ('pais', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Liga',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='Partido',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('terminado', models.BooleanField(blank=True, default=False, null=True)),
                ('fase', models.CharField(max_length=120)),
                ('liga', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asteroid.liga')),
                ('local', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='elocal', to='asteroid.equipo')),
                ('visita', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evisita', to='asteroid.equipo')),
            ],
        ),
        migrations.CreateModel(
            name='Penales',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asignado', models.IntegerField()),
                ('anotado', models.BooleanField()),
                ('contrato', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asteroid.contrato')),
                ('partido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asteroid.partido')),
            ],
        ),
        migrations.CreateModel(
            name='Goles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asignado', models.IntegerField()),
                ('minuto', models.IntegerField()),
                ('adicional', models.IntegerField()),
                ('penal', models.BooleanField()),
                ('penales', models.BooleanField()),
                ('contrato', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asteroid.contrato')),
                ('partido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asteroid.partido')),
            ],
        ),
        migrations.AddField(
            model_name='contrato',
            name='equ',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asteroid.equipo'),
        ),
        migrations.AddField(
            model_name='contrato',
            name='jug',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asteroid.jugador'),
        ),
    ]
