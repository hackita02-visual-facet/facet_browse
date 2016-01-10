
from django import forms
from django.http import HttpResponse, Http404
from django.shortcuts import redirect
from django.views.generic import CreateView, DetailView, ListView

from browse.models import FacetQuery
from . import models

class QueryForm(forms.ModelForm):
    class Meta:
        model = models.FacetQuery
        fields = (
            'query',
        )
        labels = {
            'query' :   ''
        }

class QueryCreateView(CreateView):
    model = models.FacetQuery
    form_class = QueryForm


class QueryDetailView(DetailView):
    model = models.FacetQuery

    def max_coverage(self):
        o = self.get_object()

        r = []
        for facet in o.facets.all():
            coverage = sum([k.count for k in facet.values.all()])
            r.append({
                "label"   :   facet.name,
                "value" :   coverage
            })

        return r

class FacetDetailView(DetailView):
    model = models.Facet

    def num_keys(self):
        o = self.get_object()
        return len(o.values.all())

    def count_total(self):
        o = self.get_object()
        counts = [k.count for k in o.values.all()]
        return sum(counts)

    def value_sorted(self):
        o = self.get_object()
        kv = o.values.all()

        top = sorted(kv,key=lambda x:x.count,reverse=True)

        return top

    def key_sorted_top10(self):
        kv = self.value_sorted()

        n = 10 if len(kv) >= 10 else len(kv)

        top = sorted(kv,key=lambda x:x.key)[:n]

        return top

class QueryListView(ListView):
    model = models.FacetQuery


class FacetsRenderView(DetailView):
    model = models.FacetQuery

    template_name = "browse/render_facets.html"

    def facets_data(self):
        fd = {}
        for facet in self.get_object().facets.all():
            fkv = fd[facet.name] = []
            for kv in facet.values.all():
                fkv.append({'label':kv.key,'value':kv.count})

        return fd

def render_facets(request,pk):
    try:
        print(pk)
        facet_q = FacetQuery.objects.get(pk=pk)
    except FacetQuery.DoesNotExist:
        raise Http404("Illegal query ID")

    curr_facet_ids = facet_q.deserialize_facet_ids()
    print(request.GET)
    facetval_ids = request.GET.getlist('facet',"")
    if facetval_ids:
        facetval_ids = set([int(f) for f in facetval_ids])
        facetval_ids = facetval_ids.union(curr_facet_ids)
        facetval_ids = list(facetval_ids)
        facetval_ids.sort()
        facetval_ids = FacetQuery.serialize_facet_ids(facetval_ids)

    o = FacetQuery.objects.create(query=facet_q.query,query_facets=facetval_ids)


    return redirect('render',pk=o.pk)
