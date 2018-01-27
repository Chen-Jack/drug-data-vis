from django.conf.urls import url
from django.contrib import admin
from visual.views import HomeView, get_chemical_list, get_related_side_effects, get_related_genes, get_related_chemicals

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', HomeView.as_view(), name = "home"),
    url(r'^api/chemical_list/$', get_chemical_list, name="chemical_list"),
    url(r'^api/associated_side_effects/(?P<type>\w+)/(?P<ID>\w+)/$', get_related_side_effects, name="side_effects"),
    url(r'^api/associated_genes/(?P<type>\w+)/(?P<ID>\w+)/$', get_related_genes, name="genes"),
    url(r'^api/associated_chemicals/(?P<type>\w+)/(?P<ID>\w+)/$', get_related_chemicals, name="chemicals")
]
