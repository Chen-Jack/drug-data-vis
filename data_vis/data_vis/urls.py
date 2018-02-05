from django.conf.urls import url
from django.contrib import admin
from visual.views import HomeView, get_related_side_effects, get_related_genes, get_related_chemicals, \
get_single_chem, get_single_gene, get_single_side_effect

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', HomeView.as_view(), name = "home"),
    url(r'^api/associated_side_effects/(?P<type>\w+)/(?P<ID>\w+)/$', get_related_side_effects, name="side_effects"),
    url(r'^api/associated_genes/(?P<type>\w+)/(?P<ID>\w+)/$', get_related_genes, name="genes"),
    url(r'^api/associated_chemicals/(?P<type>\w+)/(?P<ID>\w+)/$', get_related_chemicals, name="chemicals"),
    url(r'^api/chemical/(?P<ID>\w+)/$', get_single_chem, name="single_chem"),
    url(r'^api/gene/(?P<ID>\w+)/$', get_single_gene, name="single_gene"),
    url(r'^api/side_effect/(?P<ID>\w+)/$', get_single_side_effect, name="single_side_effect"),
]
