import simplejson

from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from tastypie import fields
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.exceptions import Unauthorized
from tastypie.models import ApiKey, create_api_key
from tastypie.resources import ALL, ALL_WITH_RELATIONS, ModelResource

from api.views import respond_by_audio
from core.models import Command, Page

models.signals.post_save.connect(create_api_key, sender=User)


class CheckAllNonGetAuthentication(ApiKeyAuthentication):
    """
    Authenticates everyone if the request is GET otherwise performs
    ApiKeyAuthentication.
    """

    def is_authenticated(self, request, **kwargs):
        if request.method == "GET":
            return True
        return super(CheckAllNonGetAuthentication, self).is_authenticated(
            request, **kwargs)


class CheckAllNonGetAuthorization(DjangoAuthorization):
    """
    Authorizes every authenticated user to perform GET, for all others
    performs DjangoAuthorization.
    """

    def is_authorized(self, request, object=None):
        if request.method == "GET":
            return True
        else:
            return super(CheckAllNonGetAuthorization, self).is_authorized(
                request, object)


class SingleItemModificationAuthorization(CheckAllNonGetAuthorization):
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


class CommandResource(ModelResource):
    created_by = fields.ForeignKey(UserResource, "created_by", full=True)

    class Meta:
        queryset = Command.objects.all()
        allowed_methods = ["post", "get"]
        authentication = ApiKeyAuthentication()
        authorization = SingleItemModificationAuthorization()
        excludes = ["id"]
        ordering = ["created_at"]
        always_return_data = True

    def obj_create(self, bundle, **kwargs):
        return super(CommandResource, self).obj_create(
            bundle, created_by=bundle.request.user)

    def wrap_view(self, view):
        @csrf_exempt
        def wrapper(request, *arg, **kwargs):
            callback = getattr(self, view)
            response = callback(request, *arg, **kwargs)

            if request.GET.get("format") != "voice":
                return response

            try:
                content_json = simplejson.loads(response.content)
            except simplejson.JSONDecodeError:
                return response

            # Respond by audio only when the respose is a non-JSONizable
            try:
                simplejson.loads(content_json.get("response"))
            except simplejson.JSONDecodeError:
                return respond_by_audio(content_json["response"])

            return response

        return wrapper


class PageResource(ModelResource):
    created_by = fields.ForeignKey(UserResource, "created_by", full=True)

    class Meta:
        queryset = Page.objects.all()
        allowed_methods = ["post", "get", "patch", "delete"]
        authentication = CheckAllNonGetAuthentication()
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

    def get_user(self, request):
        user = request.POST.get("user", request.GET.get("user", None))
        if user:
            return user
        key = request.POST.get("api_key", request.GET.get("api_key", None))
        try:
            a = ApiKey.objects.get(key=key)
        except ApiKey.DoesNotExist:
            return None
        return a.user

    def get_object_list(self, request):
        object_list = super(PageResource, self).get_object_list(request)
        user = self.get_user(request)
        if not user:
            return object_list.filter(status="public")
        return object_list.filter(Q(created_by=user) | Q(status="public"))

    def obj_create(self, bundle, **kwargs):
        return super(PageResource, self).obj_create(
            bundle, created_by=bundle.request.user)

    def obj_update(self, bundle, **kwargs):
        return super(PageResource, self).obj_update(
            bundle, created_by=bundle.request.user)
