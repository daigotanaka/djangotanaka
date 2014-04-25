from django.conf.urls import include, patterns, url

from tastypie.api import Api

from resources import PageResource
from views import beacon, ping

api_v1 = Api(api_name="v1")
api_v1.register(PageResource())

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'views.home', name='home'),
    # url(r'^/', include('foo.urls')),

    # My URLs
    (r"", include(api_v1.urls)),
    url(r"^v1/ping/", ping, name="ping"),
    url(r"^v1/beacon/", beacon, name="beacon"),
    # url(r"^v1/(?P<hoge>\w+)/", do_something, name="do_something")
)
