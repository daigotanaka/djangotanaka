from django.db import models
from django.contrib.auth.models import User

from tastypie.authentication import Authentication, ApiKeyAuthentication
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie.exceptions import Unauthorized
from tastypie.models import create_api_key
from tastypie.resources import ALL, ModelResource

from core.models import Page

models.signals.post_save.connect(create_api_key, sender=User)


class SingleItemModificationAuthorization(Authorization):
    def update_list(self, object_list, bundle):
        raise Unauthorized("Sorry, no bulk update.")

    def delete_list(self, object_list, bundle):
        raise Unauthorized("Sorry, no bulk delete.")

class PageResource(ModelResource):
    class Meta:
        queryset = Page.objects.all()
        allowed_methods = ["post", "get", "patch", "delete"]
        authentication = ApiKeyAuthentication()
        authorization = SingleItemModificationAuthorization()
        excludes = ["id"]
        detail_uri_name = "slug"
        filtering = {
            "slug": ALL,
            "title": ALL,
            "status": ALL,
            "body": ALL
        }
