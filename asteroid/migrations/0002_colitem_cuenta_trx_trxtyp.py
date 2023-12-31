# Generated by Django 3.1.5 on 2022-06-18 16:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('asteroid', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cuenta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=150)),
                ('tipo', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='TrxTyp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.CharField(max_length=200)),
                ('codigo', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Trx',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('monto', models.DecimalField(decimal_places=2, default=0.0, max_digits=16)),
                ('desc', models.CharField(max_length=200)),
                ('credito', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asteroid.trxtyp')),
                ('debito', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asteroid.cuenta')),
            ],
        ),
        migrations.CreateModel(
            name='ColItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('col', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asteroid.coleccion')),
                ('itm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asteroid.item')),
            ],
        ),
    ]
