# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest_auth', '0003_auto_20160508_1449'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='email',
            field=models.EmailField(unique=True, verbose_name='email address', max_length=254, default=1),
            preserve_default=False,
        ),
    ]
