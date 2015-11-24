
from django import forms
from django.views.generic import CreateView, DetailView, ListView
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

    def top_n(self,n=10):
        o = self.get_object()
        kv = o.values.all()

        n = n if len(kv) >= n else len(kv)
        top = sorted(kv,key=lambda x:x.count,reverse=True)[:n]

        return top

class QueryListView(ListView):
    model = models.FacetQuery