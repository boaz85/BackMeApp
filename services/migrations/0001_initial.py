# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmailsGrouper',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('service', models.SmallIntegerField(choices=[(0, 'Gmail'), (1, 'Google Signin'), (2, 'Google Drive'), (3, 'Dropbox')])),
                ('display_name', models.CharField(max_length=256)),
                ('uid', models.CharField(max_length=128, blank=True)),
                ('last_synced_email_uid', models.CharField(max_length=128, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='StorageTarget',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('service', models.SmallIntegerField(choices=[(0, 'Gmail'), (1, 'Google Signin'), (2, 'Google Drive'), (3, 'Dropbox')])),
                ('display_name', models.CharField(max_length=256)),
                ('uid', models.CharField(unique=True, max_length=128, blank=True)),
                ('parent_uid', models.CharField(max_length=128)),
                ('source_email_grouper', models.ForeignKey(related_name='storage_targets', to='services.EmailsGrouper')),
            ],
        ),
    ]
