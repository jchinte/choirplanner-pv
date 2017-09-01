# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Event_Planner', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='segment',
            name='visible',
            field=models.BooleanField(default=True),
        ),
    ]
