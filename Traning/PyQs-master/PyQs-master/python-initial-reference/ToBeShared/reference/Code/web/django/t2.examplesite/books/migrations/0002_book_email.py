# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-14 12:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]