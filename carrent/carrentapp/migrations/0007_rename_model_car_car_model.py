# Generated by Django 4.0.4 on 2022-05-04 08:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carrentapp', '0006_alter_usercustom_options_alter_usercustom_addr_city_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='car',
            old_name='model',
            new_name='car_model',
        ),
    ]
