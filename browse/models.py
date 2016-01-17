import json

from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db import models

from facet_core import primo

class FacetQuery(models.Model):
    query = models.CharField( max_length=150)
    query_facets = models.TextField()
    clean_query = models.ForeignKey("FacetQuery",null=True)
    year_range = models.CharField(max_length=10,null=True)
    total_hits = models.IntegerField()

    def _save_facets(self,facets):

        for name, values in facets.items():
            f = self.facets.create(name=name)

            f.values.bulk_create([
                FacetValue(facet=f,key=k,count=v) for k,v in values.items()
            ])

    @property
    def facet_ids(self):
        return json.loads(self.query_facets) if self.query_facets else []

    @staticmethod
    def serialize_facet_ids(ids):
        return json.dumps(ids)

    def get_absolute_url(self):
        return reverse("render", args=(self.pk,))

    def __str__(self):
        return "Query: {}, Total hits: {}".format(self.query,self.total_hits)

    @property
    def facet_pairs(self):

        pairs = set()
        for facet_id in self.facet_ids:
            o = FacetValue.objects.get(pk=facet_id)

            pairs.add((o.facet.name,o.key))

        if self.year_range:
            years = self.year_range.split(",")

            if years[0] == years[1]:
                years = years[0]
            else:
                years = "{} - {}".format(*years)

            pairs.add(("creationdate",years))

        return list(pairs) or None

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):

        try:
            o = FacetQuery.objects.get(query=self.query,
                                       year_range=self.year_range,
                                       query_facets=self.query_facets)
            self.pk = o.pk
        except ObjectDoesNotExist:
            res = primo.facet_query(self.query,
                                    self.facet_pairs,
                                    query_total=True)

            self.total_hits = res['total']
            if self.query_facets or self.year_range:
                self.clean_query = FacetQuery.objects.get(query=self.query,
                                                          year_range=None,
                                                          query_facets="")

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

