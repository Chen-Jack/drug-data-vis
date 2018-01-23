from django.conf.urls import url
from django.contrib import admin
from visual.views import HomeView, get_chemical_list

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', HomeView.as_view(), name = "home"),
    url(r'^api/chemical_list/$', get_chemical_list, name="chemical_list"),
]
