from django.db import models

# Create your models here.

class FacetQuery(models.Model):
    query = models.TextField(unique=True)
    facets = models.TextField()