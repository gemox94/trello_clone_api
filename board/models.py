from django.db import models
from django.utils import timezone


class Project(models.Model):

    name = models.CharField(max_length=255)
    status = models.CharField(max_length=40, null=True),
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    manager = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='projects')

    def __str__(self):
        return self.name


class Board(models.Model):

    name = models.CharField(max_length=255)
    status = models.CharField(max_length=40, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='boards')

    def __str__(self):
        return self.name


class Card(models.Model):

    name = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=40, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    board = models.ForeignKey('Board', on_delete=models.CASCADE, related_name='cards')

    def __str__(self):
        return self.name
