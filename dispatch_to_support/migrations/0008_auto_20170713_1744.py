# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-13 15:44
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dispatch_to_support', '0007_supportticket_support_person'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supportticket',
            name='support_person',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
