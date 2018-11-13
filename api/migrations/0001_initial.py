# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Guest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32)),
                ('phone_number', models.CharField(unique=True, max_length=16)),
                ('email', models.EmailField(max_length=64, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=64)),
                ('address', models.CharField(max_length=64)),
                ('time', models.DateTimeField()),
                ('limit', models.IntegerField(default=200, null=True)),
                ('status', models.IntegerField(default=0, choices=[(0, b'\xe6\x9c\xaa\xe5\xbc\x80\xe5\xa7\x8b'), (1, b'\xe8\xbf\x9b\xe8\xa1\x8c\xe4\xb8\xad'), (2, b'\xe5\xb7\xb2\xe7\xbb\x93\xe6\x9d\x9f')])),
            ],
        ),
        migrations.AddField(
            model_name='guest',
            name='meeting',
            field=models.ManyToManyField(to='api.Meeting'),
        ),
    ]
