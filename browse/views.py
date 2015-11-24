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


class FacetDetailView(DetailView):
    model = models.Facet


class QueryListView(ListView):
    model = models.FacetQuery