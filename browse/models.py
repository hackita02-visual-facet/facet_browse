
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db import models

from facet_core import primo

class FacetQuery(models.Model):
    query = models.CharField( max_length=150)
    total_hits = models.IntegerField()

    def get_facets(self):
        res = primo.facet_query(self.query, query_total=True)
        self.total_hits = res['total']

        facets = res['facets']
        for name, values in facets.items():
            f = self.facets.create(name=name)

            for k, v in values.items():
                f.values.create(key=k, count=v)

    def get_absolute_url(self):
        return reverse("query", args=(self.pk,))

    def __str__(self):
        return self.query

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        self.get_facets()


class Facet(models.Model):
    query = models.ForeignKey(FacetQuery, related_name='facets')
    name = models.CharField(max_length=100)

    def __str__(self):
        return "Query: {} - Facet: {}".format(self.query.query,self.name)

class FacetValue(models.Model):
    facet = models.ForeignKey(Facet, related_name='values')

    key = models.CharField(max_length=100)
    count = models.IntegerField()

    def __str__(self):
        return "Facet: {} - (Key: {}, Count: {})".format(self.facet.name,
                                                         self.key, self.count)

