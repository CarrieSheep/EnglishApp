# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Audio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('date', models.DateTimeField()),
                ('mp3_time', models.CharField(max_length=30)),
                ('mp3_path', models.FileField(upload_to=b'')),
                ('pic_path', models.ImageField(upload_to=b'')),
                ('content', models.TextField()),
            ],
        ),
    ]
