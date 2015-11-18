import json

from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db import models

from facet_core import primo

class FacetQuery(models.Model):
    query = models.TextField()
    facets = models.TextField()


    def get_facets(self):
        facets = primo.facet_query(self.query)
        self.facets = json.dumps(facets)

    def get_absolute_url(self):
        return reverse("query", args=(self.pk,))

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        try:
            o =  FacetQuery.objects.get(query=self.query)
            self.pk = o.pk
            self.facets = o.facets
        except ObjectDoesNotExist:
            self.get_facets()
            super().save(force_insert, force_update, using, update_fields)

