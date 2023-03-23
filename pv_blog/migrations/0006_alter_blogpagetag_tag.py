# Generated by Django 4.1.5 on 2023-01-09 23:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0005_auto_20220424_2025'),
        ('pv_blog', '0005_auto_20210213_1444'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpagetag',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_items', to='taggit.tag'),
        ),
    ]