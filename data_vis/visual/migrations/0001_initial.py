# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-20 20:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chemical',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CID', models.IntegerField()),
                ('InChIKey', models.CharField(max_length=27)),
                ('SMILES', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='SideEffect',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('UMLS_CUI', models.CharField(max_length=8)),
            ],
        ),
    ]
