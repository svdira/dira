# Generated by Django 4.2.2 on 2024-05-31 20:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('asteroid', '0029_mlbteam_mlbgame'),
    ]

    operations = [
        migrations.CreateModel(
            name='matchSquad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('equipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asteroid.equipo')),
                ('partido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asteroid.partido')),
            ],
        ),
        migrations.CreateModel(
            name='squadPlayers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(max_length=1)),
                ('jugador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asteroid.contrato')),
                ('squad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asteroid.matchsquad')),
            ],
        ),
    ]