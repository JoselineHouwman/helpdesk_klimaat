# Generated by Django 2.2.9 on 2020-01-12 10:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('experts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='expert',
            name='profile_picture',
        ),
    ]
