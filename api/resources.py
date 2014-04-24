from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

from tastypie import fields
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized
from tastypie.models import create_api_key
from tastypie.resources import ALL, ALL_WITH_RELATIONS, ModelResource

from core.models import Page

models.signals.post_save.connect(create_api_key, sender=User)


class SingleItemModificationAuthorization(Authorization):
    def update_list(self, object_list, bundle):
        raise Unauthorized("Sorry, no bulk update.")

    def delete_list(self, object_list, bundle):
        raise Unauthorized("Sorry, no bulk delete.")

    def read_list(self, object_list, bundle):
        return object_list.filter(created_by=bundle.request.user)


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        allowed_methods = []
        excludes = [
            "email",
            "password",
            "is_active",
            "is_staff",
            "is_superuser"
        ]
        filtering = {
            "username": ALL
        }


class PageResource(ModelResource):
    created_by = fields.ForeignKey(UserResource, "created_by", full=True)

    class Meta:
        queryset = Page.objects.all()
        allowed_methods = ["post", "get", "patch", "delete"]
        authentication = ApiKeyAuthentication()
        authorization = SingleItemModificationAuthorization()
        excludes = ["id"]
        detail_uri_name = "slug"
        filtering = {
            "created_by": ALL_WITH_RELATIONS,
            "slug": ALL,
            "title": ALL,
            "status": ALL,
            "body": ALL
        }
        ordering = ["created_at", "modified_at", "slug", "title", "status"]

    def obj_create(self, bundle, **kwargs):
        return super(PageResource, self).obj_create(
            bundle, created_by=bundle.request.user)

    def obj_update(self, bundle, **kwargs):
        return super(PageResource, self).obj_update(
            bundle, created_by=bundle.request.user)
