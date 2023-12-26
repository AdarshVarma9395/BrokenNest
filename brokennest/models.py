from django.db import models

# Create your models here.
class books(models.Model):
    note_name = models.CharField(max_length = 200)
    note_description = models.TextField()