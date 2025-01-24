from email.policy import default
from enum import unique

from django.db import models

class Women(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(unique=True, blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    slug = models.SlugField(max_length=255, default='', blank=True)

    def __str__(self):
        return self.title



