# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SongManager', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('send_reminder', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField()),
                ('title', models.CharField(max_length=100, blank=True)),
                ('is_template', models.BooleanField(default=False)),
            ],
            options={
                'permissions': (('can_create_template', 'Can create an event template'),),
            },
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=80)),
            ],
        ),
        migrations.CreateModel(
            name='Segment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField()),
                ('title', models.CharField(max_length=100, blank=True)),
                ('notes', models.TextField(blank=True)),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='LinkedSegment',
            fields=[
                ('segment_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='Event_Planner.Segment')),
                ('link', models.URLField()),
            ],
            bases=('Event_Planner.segment',),
        ),
        migrations.CreateModel(
            name='SongSegment',
            fields=[
                ('segment_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='Event_Planner.Segment')),
                ('song', models.ForeignKey(blank=True, to='SongManager.Song', null=True)),
            ],
            bases=('Event_Planner.segment',),
        ),
        migrations.AddField(
            model_name='segment',
            name='event',
            field=models.ForeignKey(to='Event_Planner.Event'),
        ),
        migrations.AddField(
            model_name='participant',
            name='roles',
            field=models.ManyToManyField(to='Event_Planner.Role', through='Event_Planner.Activity'),
        ),
        migrations.AddField(
            model_name='activity',
            name='participant',
            field=models.ForeignKey(to='Event_Planner.Participant'),
        ),
        migrations.AddField(
            model_name='activity',
            name='role',
            field=models.ForeignKey(to='Event_Planner.Role'),
        ),
        migrations.AddField(
            model_name='activity',
            name='segment_event',
            field=models.ForeignKey(to='Event_Planner.Segment'),
        ),
    ]
