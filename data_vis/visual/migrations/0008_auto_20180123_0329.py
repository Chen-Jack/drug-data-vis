# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-23 03:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visual', '0007_sideeffect_causedby'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sideeffect',
            old_name='causedby',
            new_name='caused_by',
        ),
    ]