# Generated by Django 4.2.2 on 2023-11-15 16:54

import asteroid.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('asteroid', '0024_personadt'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contrato',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('position', models.CharField(default='Not Specified', max_length=256)),
                ('number', models.IntegerField(default=0)),
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
                ('biographics', models.TextField(default='This section needs to be expanded.')),
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
            name='PartidoComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comm', models.TextField()),
                ('comm_partido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asteroid.partido')),
            ],
        ),
        migrations.CreateModel(
            name='LigaTeams',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flagActivo', models.BooleanField(default=True)),
                ('equipoRel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asteroid.equipo')),
                ('ligaRel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asteroid.liga')),
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
                ('og', models.BooleanField(default=False)),
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
