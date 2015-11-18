from django.shortcuts import render
import json
from django.views.generic import CreateView, DetailView
from django.core.urlresolvers import reverse_lazy

from . import models

from facet_core import primo

# Create your views here.

class Query(CreateView,DetailView):
    model = models.FacetQuery

    fields = (
        'query',
    )

    success_url = reverse_lazy("query",args=[object.pk])

    def form_valid(self,form):
        qs = super().get_queryset().filter(
            query = form.instance.query
        )

        if qs:
            form.instance.facets = qs[0].facets
        else:
            fcs = primo.facet_query(
                form.instance.query
            )

            form.instance.facets = json.dumps(fcs)



