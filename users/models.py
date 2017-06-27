# -*- coding: utf-8 -*-
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from users.managers import UsersManager


@python_2_unicode_compatible
class User(AbstractBaseUser, PermissionsMixin):

    USERNAME_FIELD = 'email'

    objects = UsersManager()

    first_name = models.CharField(blank=True, max_length=255)

    last_name = models.CharField(blank=True, max_length=255)

    email = models.EmailField(unique=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def get_short_name(self):
        return self.first_name + ' ' + self.last_name

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    @property
    def is_staff(self):
        return self.is_superuser