# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-23 00:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visual', '0003_sideeffect'),
    ]

    operations = [
        migrations.AddField(
            model_name='sideeffect',
            name='causedBy',
            field=models.ManyToManyField(blank=True, null=True, to='visual.Chemical'),
        ),
    ]
