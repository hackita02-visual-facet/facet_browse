from django.conf.urls import include, url
from django.contrib import admin

from browse import views

urlpatterns = [
    url(r'^admin/$', include(admin.site.urls)),
    url(r'^$',views.QueryCreateView.as_view(),name="add_query"),
    url(r'^queries$',views.QueryListView.as_view(),name="list_queries"),
    url(r'^query/(?P<pk>\d+)',views.QueryDetailView.as_view(),name="query"),
    url(r'^facet/(?P<pk>\d+)',views.FacetDetailView.as_view(),name="facet"),
]
