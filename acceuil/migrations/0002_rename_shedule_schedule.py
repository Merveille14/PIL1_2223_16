# Generated by Django 4.2.2 on 2023-07-02 23:24

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('authentification', '0006_alter_myuser_first_name_alter_myuser_last_name'),
        ('acceuil', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Shedule',
            new_name='Schedule',
        ),
    ]
