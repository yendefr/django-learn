from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')

class Post(models.Model):
    objects = models.Manager()
    published = PublishedManager()

    STATUS_CHOISES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=64)
    slug = models.SlugField(max_length=64, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOISES, default='draft')

    class Meta:
        ordering = (
            '-publish',
        )
    
    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year,
                                                 self.publish.month,
                                                 self.publish.day,
                                                 self.slug])

    def __str__(self):
        return self.title
