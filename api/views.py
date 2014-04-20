import logging
import simplejson

from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from core.models import Page

logger = logging.getLogger(__name__)


def ping(request):
    response = {"status": "ok"}
    return HttpResponse(simplejson.dumps(response))
