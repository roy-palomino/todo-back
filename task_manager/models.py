from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True, default='')
    background_color = models.CharField(
        max_length=100, null=True, default='white')
    text_color = models.CharField(max_length=100, blank=True, default='black')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True, default='')
    done = models.BooleanField(default=False)
    owner = models.ForeignKey(
        'auth.User', related_name='tasks', on_delete=models.CASCADE)
    due_date = models.DateTimeField(null=True, blank=True)
    is_important = models.BooleanField(default=False)
    is_urgent = models.BooleanField(default=False)
    categories = models.ManyToManyField(
        Category, related_name='tasks', blank=True)
    tags = models.ManyToManyField(
        Tag, related_name='tasks', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.name
