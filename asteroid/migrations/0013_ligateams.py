# Generated by Django 4.0.6 on 2023-05-28 22:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('asteroid', '0012_notes'),
    ]

    operations = [
        migrations.CreateModel(
            name='LigaTeams',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flagActivo', models.BooleanField(default=True)),
                ('equipoRel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asteroid.equipo')),
                ('ligaRel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asteroid.liga')),
            ],
        ),
    ]
