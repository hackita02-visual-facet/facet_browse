
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db import models

from facet_core import primo

class FacetQuery(models.Model):
    query = models.CharField( max_length=150)
    query_facets = models.TextField()
    total_hits = models.IntegerField()

    def _save_facets(self,facets):

        for name, values in facets.items():
            f = self.facets.create(name=name)

            f.values.bulk_create([
                FacetValue(facet=f,key=k,count=v) for k,v in values.items()
            ])

    def _facet_pairs(self):
        pass

    def _canonize_facets(self):
        pass

    def get_absolute_url(self):
        return reverse("query", args=(self.pk,))

    def __str__(self):
        return "Query: {}, Total hits: {}".format(self.query,self.total_hits)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):

        try:
            o = FacetQuery.objects.get(query=self.query,query_facets=self.query_facets)
            self.pk = o.pk
        except ObjectDoesNotExist:
            res = primo.facet_query(self.query,
                                    self._facet_pairs(),
                                    query_total=True)

            self._canonize_facets()
            self.total_hits = res['total']

            super().save(force_insert, force_update, using, update_fields)

            self._save_facets(res['facets'])


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

