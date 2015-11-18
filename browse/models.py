
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db import models

from facet_core import primo

class FacetQuery(models.Model):
    query = models.TextField()


    def get_facets(self):
        facets = primo.facet_query(self.query)

        for f_name,fs in facets.items():
            f_obj = Facet.objects.create(name=f_name,query=self)

            for k,v in fs.items():
                FacetValue.objects.create(facet=f_obj,key=k,count=v)

    def get_absolute_url(self):
        return reverse("query", args=(self.pk,))

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        try:
            o =  FacetQuery.objects.get(query=self.query)
            self.pk = o.pk
        except ObjectDoesNotExist:
            super().save(force_insert, force_update, using, update_fields)
            self.get_facets()

    def __str__(self):
        return self.query

class Facet(models.Model):
    name = models.CharField(max_length=100)
    query = models.ForeignKey(FacetQuery)

    def __str__(self):
        return "Query: {} - Facet: {}".format(self.query.query,self.name)

class FacetValue(models.Model):
    facet = models.ForeignKey(Facet)

    key = models.CharField(max_length=100)
    count = models.IntegerField()

    def __str__(self):
        return "Facet: {} - (Key: {}, Count: {})".format(self.face.name,
                                                         self.key,self.count)

