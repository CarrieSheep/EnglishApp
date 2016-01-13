# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_audioinfo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audioinfo',
            name='mp3_time',
            field=models.CharField(max_length=30),
        ),
    ]
