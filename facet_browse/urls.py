from django.conf.urls import include, url
from django.contrib import admin

from browse import views

urlpatterns = [
    url(r'^admin/$', include(admin.site.urls)),
    url(r'^query/$',views.QueryCreateView.as_view(),name="add_query"),
    url(r'^query/(?P<pk>\d+)',views.QueryDetailView.as_view(),name="query")
]
