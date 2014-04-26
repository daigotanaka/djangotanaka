import logging
import simplejson
import urllib

from django.contrib.auth.models import User
from django.http import Http404, HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from core.models import Page
from core.commands import execute_command
from tastypie.models import ApiKey

logger = logging.getLogger(__name__)


def ping(request):
    response = {"status": "ok"}
    return HttpResponse(simplejson.dumps(response))


def respond_by_audio(message):
    param = urllib.urlencode({"tl": "en", "q": message})
    url = "http://translate.google.com/translate_tts?" + param
    return HttpResponseRedirect(url)

@csrf_exempt
def beacon(request):
    if request.method != "POST":
        return HttpResponseForbidden()

    user = User.objects.get(username=request.GET.get("username"))
    api_key = ApiKey.objects.get(user=user)
    if not user or not api_key or api_key.key != request.GET.get("api_key"):
        raise Http404

    ret_format = request.GET.get("format")
    data = {
        "lat": request.POST.get("lat"),
        "lng": request.POST.get("lng")
    }

    class BeaconCommand(object):
        created_by = user
        name = "beacon"
        raw_command = None
        data = None

    command = BeaconCommand()
    command.data = simplejson.dumps(data)
    name, response = execute_command(command)
    if ret_format == "voice" and not type(response) is dict:
        return respond_by_audio(response)

    try:
        return HttpResponse(simplejson.dumps(response))
    except simplejson.JSONDecodeError:
        raise Exception
