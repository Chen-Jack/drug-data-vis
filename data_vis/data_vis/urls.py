from django.conf.urls import url
from django.contrib import admin
from visual.views import HomeView, chemical_side_effects, get_chemical_list

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', HomeView.as_view(), name = "home"),
    url(r'^api/side_effect_data/$', chemical_side_effects, name="chemical_side_effects" ),
    url(r'^api/chemical_list/$', get_chemical_list, name="chemical_list"),
]
