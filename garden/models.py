from django.db import models
from datetime import datetime
from system.storage import ImageStorage
from django.db import models
from django.utils import timezone
import os
from uuid import uuid4
from django.db.models import Q, Avg, Count, Min, Sum
from random import choice

def media_path(instance, filename):
    upload_to = 'garden'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)

class Petal(models.Model):
	imagen = models.ImageField(upload_to=media_path, max_length=255, null=True, blank=True)
	ptags = models.CharField(max_length=512)

	def __str__(self):
		return self.ptags

class Tags(models.Model):
	petal = models.ForeignKey(Petal, on_delete = models.CASCADE)
	tag = models.CharField(max_length=100)
	def __str__(self):
		return self.tag