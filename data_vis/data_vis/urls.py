from django.conf.urls import url
from django.contrib import admin
from visual.views import HomeView, chemical_side_effects

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', HomeView.as_view(), name = "home"),
    url(r'^api/side_effect_data/$', chemical_side_effects, name="chemical_side_effects" )
]
