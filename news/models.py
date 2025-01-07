from django.db import models
from django.utils import timezone

class News(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    url = models.URLField()
    image_url = models.URLField(blank=True, null=True)
    source_name = models.CharField(max_length=100)
    published_at = models.DateTimeField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-published_at']
        verbose_name = 'News Article'
        verbose_name_plural = 'News Articles'
        indexes = [
            models.Index(fields=['-published_at']),
        ]

    def __str__(self):
        return self.title
