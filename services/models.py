from django.db import models

from backmeapp.settings import ServicesData
from users.models import User


class EmailsGrouper(models.Model):

    service = models.SmallIntegerField(choices=ServicesData.get_choices())

    user = models.ForeignKey(User, related_name='email_groupers')

    display_name = models.CharField(max_length=256)

    uid = models.CharField(max_length=128, blank=True)

    last_synced_email_uid = models.CharField(max_length=128, blank=True)


class StorageTarget(models.Model):

    service = models.SmallIntegerField(choices=ServicesData.get_choices())

    display_name = models.CharField(max_length=256)

    uid = models.CharField(max_length=128, unique=True, blank=True)

    parent_uid = models.CharField(max_length=128)

    source_email_grouper = models.ForeignKey(EmailsGrouper, related_name='storage_targets')