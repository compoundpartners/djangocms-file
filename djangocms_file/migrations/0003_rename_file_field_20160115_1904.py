# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-16 00:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_file', '0002_auto_20151202_1551'),
    ]

    operations = [
        migrations.RenameField('file', 'file', 'source')
    ]