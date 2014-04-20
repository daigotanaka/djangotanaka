import requests
import simplejson

from optparse import make_option

import django.contrib.auth.hashers as hashers

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from site_info import WEBSITE_URL

API_URL = WEBSITE_URL + "/api/v1"


class Command(BaseCommand):
    args = "pull/push filename"
    help = "Pull/push page"

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
        self.pull(
            username=settings.DJANGO_USERNAME,
            api_key=settings.DJANGO_API_KEY,
            slug=options["slug"],
            title=options["title"],
            status=options["status"]
        )
        return

    def pull(self, username, api_key, slug=None, title=None, status=None):
        data = {
            "username": username,
            "api_key": api_key,
            "slug": slug,
            "title": title,
            "status": status
        }
        response = requests.get(API_URL + "/page/", params=data)

        pages = simplejson.loads(response.text).get("objects")
        for page in pages:
            print page.get("slug")
            with open(page.get("slug") + ".txt", "w") as f:
                try:
                    f.write(page.get("body"))
                except UnicodeEncodeError, err:
                    print err
