from django.conf.urls import url
from django.contrib import admin
from visual.views import HomeView, get_chemical_list, get_related_side_effects, get_related_genes

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', HomeView.as_view(), name = "home"),
    url(r'^api/chemical_list/$', get_chemical_list, name="chemical_list"),
    url(r'^api/side_effects/(?P<CID>[0-9]*)/$', get_related_side_effects, name="side_effects"),
    url(r'^api/genes/(?P<CID>[0-9]*)/$', get_related_genes, name="genes")
]
