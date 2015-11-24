from django import forms
from django.forms import TextInput
from django.views.generic import CreateView, DetailView

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