# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('rest_auth', '0002_myuser_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='date_joined',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined'),
        ),
        migrations.AddField(
            model_name='myuser',
            name='is_staff',
            field=models.BooleanField(default=False, verbose_name='staff status', help_text='Designates whether the user can log into this admin site.'),
        ),
    ]
