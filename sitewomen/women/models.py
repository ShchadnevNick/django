from django.db import models

class PublishedModel(models.Manager):
    def get_queryset(self):
        return super().get_queryset.filter(is_published=Women.Status.PUBLISHED)

class Women(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length=255)
    content = models.TextField(unique=True, blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    slug = models.SlugField(max_length=255, default='', blank=True)
    objects = models.Manager()
    published = PublishedModel()

    def __str__(self):
        return self.title




