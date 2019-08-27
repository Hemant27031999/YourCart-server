from django.db import models

# Create your models here.
class Topic(models.Model):
    # top_name = models.CharField(max_length=264, unique=True)

    def __init__(self, name):
        self.top_name = name

    def __str__(self):
        return self.top_name
