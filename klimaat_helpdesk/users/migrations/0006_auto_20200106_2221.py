# Generated by Django 2.2.8 on 2020-01-06 22:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_expertprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expertprofile',
            name='profile_picture',
            field=models.FileField(blank=True, upload_to='', verbose_name='Picture'),
        ),
        migrations.AlterField(
            model_name='expertprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='expert_profile', to=settings.AUTH_USER_MODEL),
        ),
    ]