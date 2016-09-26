# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-19 16:54


import random
import json

from django.db import migrations


def add_personality(apps, schema_editor):
    for person in apps.get_model("persons", "Person").objects.all().iterator():
        data = json.loads(person.data)

        data['personality'] = {'cosmetic': random.randint(0, 9),
                               'practical': random.randint(1, 14)}

        person.data = json.dumps(data, ensure_ascii=True)

        person.save()


class Migration(migrations.Migration):

    dependencies = [
        ('persons', '0006_remove_all_social_connections'),
    ]

    operations = [
        migrations.RunPython(add_personality)
    ]
