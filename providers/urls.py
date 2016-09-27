from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns

from providers import views


urlpatterns = [
    url(r'^providers/$', views.ProviderListView.as_view()),
    url(r'^providers/get_token$', views.GenerateTokenView.as_view()),
    url(r'^providers/(?P<pk>[0-9]+)$', views.ProviderDetailView.as_view()),
    url(r'^areas/$', views.ServiceAreaListView.as_view()),
    url(r'^areas/(?P<pk>[0-9]+)$', views.ServiceAreaDetailView.as_view()),
    url(r'^get_areas/$', views.ServiceAreaQueryView.as_view()),
    url(r'^docs/', include('rest_framework_docs.urls')),
]

urlpatterns = format_suffix_patterns(urlpatterns)
