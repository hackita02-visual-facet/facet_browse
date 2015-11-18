from django import forms
from django.views.generic import CreateView, DetailView

from . import models

class QueryForm(forms.ModelForm):
    class Meta:
        model = models.FacetQuery
        fields = (
            'query',
        )

class QueryCreateView(CreateView):
    model = models.FacetQuery
    form_class = QueryForm


class QueryDetailView(DetailView):
    model = models.FacetQuery

    def form(self):
        return QueryForm(initial={
            'query': self.get_object().query
        })
