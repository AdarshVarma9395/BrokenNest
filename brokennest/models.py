from django.db import models
from django.contrib.auth.models import User



class books(models.Model):
    user = models.ForeignKey(User,on_delete = models.SET_NULL, null=True,blank=True)
    note_name = models.CharField(max_length = 200)
    note_description = models.TextField()
    created_time = models.DateTimeField(null=True)