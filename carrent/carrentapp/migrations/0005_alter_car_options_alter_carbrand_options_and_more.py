# Generated by Django 4.0.4 on 2022-05-04 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carrentapp', '0004_carbrand_carmodel_car'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='car',
            options={'verbose_name': 'Samochód', 'verbose_name_plural': 'Samochody'},
        ),
        migrations.AlterModelOptions(
            name='carbrand',
            options={'verbose_name': 'Marka', 'verbose_name_plural': 'Marki'},
        ),
        migrations.AlterModelOptions(
            name='carmodel',
            options={'verbose_name': 'Model', 'verbose_name_plural': 'Modele'},
        ),
        migrations.AlterField(
            model_name='car',
            name='car_image',
            field=models.ImageField(upload_to='images/cars', verbose_name='Zdjęcie'),
        ),
        migrations.AlterField(
            model_name='car',
            name='car_mileage',
            field=models.IntegerField(verbose_name='Przebieg'),
        ),
        migrations.AlterField(
            model_name='car',
            name='color',
            field=models.CharField(max_length=50, verbose_name='Kolor'),
        ),
        migrations.AlterField(
            model_name='car',
            name='engine_power',
            field=models.IntegerField(verbose_name='Moc'),
        ),
        migrations.AlterField(
            model_name='car',
            name='engine_type',
            field=models.CharField(choices=[('Benzynowy', 'Benzynowy'), ('Diesel', 'Diesel'), ('Elektryczny', 'Elektryczny'), ('Hybryda', 'Hybryda')], max_length=20, verbose_name='Rodzaj silnika'),
        ),
        migrations.AlterField(
            model_name='car',
            name='gearbox_type',
            field=models.CharField(choices=[('Automatyczna', 'Automatyczna'), ('Manualna', 'Manualna')], max_length=15, verbose_name='Skrzynia biegów'),
        ),
        migrations.AlterField(
            model_name='car',
            name='number_of_seats',
            field=models.IntegerField(verbose_name='Ilość miejsc'),
        ),
        migrations.AlterField(
            model_name='car',
            name='plate_number',
            field=models.CharField(max_length=20, unique=True, verbose_name='Numer rejestracyjny'),
        ),
        migrations.AlterField(
            model_name='car',
            name='rating',
            field=models.FloatField(verbose_name='Ocena'),
        ),
        migrations.AlterField(
            model_name='car',
            name='year_of_production',
            field=models.IntegerField(verbose_name='Rok produkcji'),
        ),
        migrations.AlterField(
            model_name='carbrand',
            name='brand_name',
            field=models.CharField(max_length=50, unique=True, verbose_name='Marka'),
        ),
    ]
