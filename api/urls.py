from django.conf.urls import include, patterns, url

from tastypie.api import Api

from resources import PageResource
from views import ping

api_v1 = Api(api_name="v1")
api_v1.register(PageResource())

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'views.home', name='home'),
    # url(r'^/', include('foo.urls')),

    # My URLs
    (r"", include(api_v1.urls)),
    url(r"^ping/", ping, name="ping")
)
