from django.db import models
from django.contrib.postgres.fields import ArrayField


class Project(models.Model):
    class Meta:
        db_table = "projects"
        ordering = ['-created_at']
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    title = models.CharField(max_length=50)
    date_event = models.DateField()
    brief_description = models.CharField(max_length=250)
    location = models.CharField(max_length=100)
    photo_1 = models.ImageField(blank=True)
    text_1_intro = models.TextField(blank=True)
    photo_2 = models.ImageField(blank=True)
    text_2 = models.TextField(blank=True)
    author = models.CharField(max_length=20, blank=True)
    editor = models.CharField(max_length=20, blank=True)
    svitliny = ArrayField(models.ImageField(), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
