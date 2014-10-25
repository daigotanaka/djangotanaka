from django.conf.urls import include, patterns, url

from tastypie.api import Api

from resources import CommandResource, PageResource
from views import beacon, ping

api_v1 = Api(api_name="v1")
api_v1.register(PageResource())
api_v1.register(CommandResource())

urlpatterns = patterns(
    "",
    (r"", include(api_v1.urls)),
    url(r"^v1/ping/", ping, name="ping"),
    url(r"^v1/beacon/", beacon, name="beacon"),
)
