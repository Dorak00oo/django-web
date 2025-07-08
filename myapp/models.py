from django.db import models
from django.contrib.auth.models import User


class project(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='projects'   # opcional, para acceder como user.projects.all()
    )

    def __str__(self):
        return self.name

class task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    project = models.ForeignKey(project, on_delete=models.CASCADE)
    done = models.BooleanField(default=False)

    def __str__(self):
        return self.title + ' - ' + self.project.name
