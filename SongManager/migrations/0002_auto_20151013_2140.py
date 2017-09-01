# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SongManager', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='composers',
            field=models.ManyToManyField(to='SongManager.Composer', blank=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='tags',
            field=models.ManyToManyField(to='SongManager.Tag', blank=True),
        ),
    ]
