# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2018-04-01 15:34
from __future__ import unicode_literals

from django.db import migrations


def remove_middle_gender(apps, schema_editor):
    apps.get_model("accounts", "Account").objects.filter(gender=2).update(gender=0)


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_remove_preferences_purchases'),
        ('heroes', '0023_remove_middle_gender'),
    ]

    operations = [
        migrations.RunPython(
            remove_middle_gender,
        ),
    ]