import os
import requests
import simplejson

from optparse import make_option

import django.contrib.auth.hashers as hashers

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from site_info import WEBSITE_URL

API_URL = WEBSITE_URL + "/api/v1"


class Command(BaseCommand):
    args = "patch filename"
    help = "Patch page"

    option_list = BaseCommand.option_list + (
        make_option("--slug",
            dest="slug",
            default=None,
            help=""),
        make_option("--title",
            dest="title",
            default=None,
            help=""),
         make_option("--status",
            dest="status",
            default=None,
            help="")
        )

    def handle(self, *args, **options):
        filename = args[0]
        if not os.path.exists(filename):
            return
        with open(filename) as f:
            body = f.read()
        _, name = os.path.split(filename)
        pos = name.find(".")
        slug = name[0:pos] if pos > 0 else filename
        self.patch(
            username=settings.DJANGO_USERNAME,
            api_key=settings.DJANGO_API_KEY,
            slug=slug,
            body=body,
            title=options["title"] or slug,
            status=options["status"] or "private"
        )
        return

    def patch(self, username, api_key, slug, body, title, status="private"):
        params = {
            "username": username,
            "api_key": api_key,
        }
        data = {
            "body": body,
            "title": title,
            "status": status,
        }
        print slug
        headers = {"content-type": "application/json"}
        # response = requests.patch(API_URL + "/page/", params=params, data=data)
        response = requests.patch(API_URL + "/page/" + slug + "/", headers=headers, params=params, data=simplejson.dumps(data))
        print response
