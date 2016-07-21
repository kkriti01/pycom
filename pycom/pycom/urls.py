from django.conf.urls import url
from django.contrib import admin

from business.views import BusinessListView, PopulateBusiness

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', BusinessListView.as_view(), name='home'),
    url(r'^populate-business', PopulateBusiness.as_view(), name='populate_business'),
]
