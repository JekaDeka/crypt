# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-09-20 15:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crypt', '0004_remove_post_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='crypted_text',
            field=models.TextField(default=None),
        ),
    ]