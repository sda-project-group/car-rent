# Generated by Django 4.0.4 on 2022-04-26 12:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0003_logentry_add_action_flag_choices'),
        ('carrentapp', '0002_rename_usercustom_user'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User',
            new_name='UserCustom',
        ),
    ]
