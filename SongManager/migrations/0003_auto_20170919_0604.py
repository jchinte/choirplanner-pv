# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SongManager', '0002_auto_20151013_2140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='songfile',
            name='file',
            field=models.FileField(upload_to='songs'),
        ),
    ]
