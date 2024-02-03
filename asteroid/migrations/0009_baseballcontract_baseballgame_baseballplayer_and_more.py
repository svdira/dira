# Generated by Django 4.0.6 on 2023-03-31 23:49

import asteroid.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('asteroid', '0008_partidocomment'),
    ]

    operations = [
        migrations.CreateModel(
            name='baseballContract',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='baseballGame',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('l_runs', models.IntegerField()),
                ('v_runs', models.IntegerField()),
                ('innings', models.IntegerField()),
                ('gameDate', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='baseballPlayer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=128)),
                ('info', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='baseballTeam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=128)),
                ('ciudad', models.CharField(max_length=128)),
                ('logo', models.ImageField(blank=True, max_length=255, null=True, upload_to=asteroid.models.path_and_name)),
            ],
        ),
        migrations.CreateModel(
            name='baseballGamePitch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.FloatField()),
                ('h', models.IntegerField()),
                ('cl', models.IntegerField()),
                ('bb', models.IntegerField()),
                ('p', models.IntegerField()),
                ('bGame', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asteroid.baseballgame')),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asteroid.baseballcontract')),
            ],
        ),
        migrations.CreateModel(
            name='baseballGameBat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ab', models.IntegerField()),
                ('r', models.IntegerField()),
                ('h', models.IntegerField()),
                ('bb', models.IntegerField()),
                ('cp', models.IntegerField()),
                ('hr', models.IntegerField()),
                ('bGame', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asteroid.baseballgame')),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asteroid.baseballcontract')),
            ],
        ),
        migrations.AddField(
            model_name='baseballgame',
            name='local',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='local_t', to='asteroid.baseballteam'),
        ),
        migrations.AddField(
            model_name='baseballgame',
            name='visit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='visit_t', to='asteroid.baseballteam'),
        ),
        migrations.AddField(
            model_name='baseballcontract',
            name='bPlayer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asteroid.baseballplayer'),
        ),
        migrations.AddField(
            model_name='baseballcontract',
            name='bTeam',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asteroid.baseballteam'),
        ),
    ]
