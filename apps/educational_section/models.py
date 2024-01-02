from django.db import models


class EducationalSection(models.Model):
    class Meta:
        db_table = "educational_sections"
        ordering = ['-created_at']
        verbose_name = "Educational section"
        verbose_name_plural = "Educational sections"

    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    photo1 = models.ImageField(blank=True)
    photo2 = models.ImageField(blank=True)
    photo3 = models.ImageField(blank=True)
    photo4 = models.ImageField(blank=True)
    photo5 = models.ImageField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
