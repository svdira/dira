# Generated by Django 3.1.5 on 2022-07-02 14:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('asteroid', '0004_auto_20220620_1441'),
    ]

    operations = [
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('anho', models.IntegerField()),
                ('mes', models.IntegerField()),
                ('mbudget', models.DecimalField(decimal_places=2, default=0.0, max_digits=16)),
                ('cuenta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asteroid.trxtyp')),
            ],
        ),
    ]
