# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-19 14:49


from django.db import migrations


def remove_person_leave_place_message(apps, schema_editor):
    Template = apps.get_model("linguistics", "Template")
    Template.objects.filter(key=260014).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('linguistics', '0015_remove_technical_template_parts'),
    ]

    operations = [
        migrations.RunPython(
            remove_person_leave_place_message,
        ),
    ]
