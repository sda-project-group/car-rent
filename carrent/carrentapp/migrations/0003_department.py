# Generated by Django 4.0.4 on 2022-05-21 09:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('carrentapp', '0002_remove_order_car_brand_remove_order_car_model_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('addr_loc_country', models.CharField(choices=[('pl', 'Polska')], max_length=50, verbose_name='Kraj oddziału')),
                ('addr_loc_city', models.CharField(choices=[('WAW', 'Warszawa'), ('KRK', 'Kraków'), ('KTW', 'Katowice'), ('WRO', 'Wrocław')], max_length=50, verbose_name='Miasto oddziału')),
                ('addr_loc_street', models.CharField(max_length=50, verbose_name='Ulica')),
                ('addr_loc_post_code', models.CharField(max_length=6, verbose_name='Kod pocztowy')),
                ('bm_supervisor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Kierownik')),
            ],
            options={
                'verbose_name': 'Oddział',
                'verbose_name_plural': 'Oddziały',
            },
        ),
    ]
