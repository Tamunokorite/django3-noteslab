from django.db import models
from django.db.models.fields import DateTimeField
from django.urls import reverse

# Create your models here.
class Note(models.Model):
    title = models.CharField(max_length=150)
    content = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)
    date_deleted = models.DateTimeField(null=True)

    class Meta:
        verbose_name = ("Note")
        verbose_name_plural = ("Notes")

    def __str__(self):
        return self.title