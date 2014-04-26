import logging
import simplejson
import urllib

from django.contrib.auth.models import User
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from core.models import Page
from core.commands import execute_command
from tastypie.models import ApiKey

logger = logging.getLogger(__name__)


def ping(request):
    response = {"status": "ok"}
    return HttpResponse(simplejson.dumps(response))


def beacon(request):
    user = User.objects.get(username=request.GET.get("username"))
    api_key = ApiKey.objects.get(user=user)
    if not user or not api_key or api_key.key != request.GET.get("api_key"):
        raise Http404

    name, response = execute_command(None, response.GET)
    if not type(response) is dict:
        param = urllib.urlencode({"tl": "en", "q": response})
        url = "http://translate.google.com/translate_tts?" + param
        return HttpResponseRedirect(url)

    try:
        return HttpResponse(simplejson.dumps(response))
    except simplejson.JSONDecodeError:
        raise Exception
