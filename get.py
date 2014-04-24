import os
import requests
import simplejson

from site_info import WEBSITE_URL

API_URL = WEBSITE_URL + "/api/v1"


class Command(object):

    def get(self, username, api_key):
        params = {
            "username": username,
            "api_key": api_key,
            "slug": self.slug,
            "title": self.title,
            "status": self.status,
            "order_by": "-modified_at"
        }

        headers = {"content-type": "application/json"}
        # response = requests.patch(API_URL + "/page/", params=params, data=data)
        response = requests.get(
                API_URL + "/page/",
                headers=headers,
                params=params,
            )

        pages = simplejson.loads(response.text).get("objects")
        for page in pages:
            print page.get("slug")
            with open(page.get("slug") + ".txt", "w") as f:
                try:
                    f.write(page.get("body").encode("utf-8"))
                except UnicodeEncodeError, err:
                    print err


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Patch update an existing page")
    parser.add_argument(
        "--title",
        dest="title",
        action="store",
        default=None,
        help="Store the title to be updated"
    )
    parser.add_argument(
        "--status",
        dest="status",
        action="store",
        default=None,
        help="Store the status (public|private) to be updated"
    )
    parser.add_argument(
        "--slug",
        dest="slug",
        action="store",
        default=None,
        help="Store the slug to be updated"
    )

    c = Command()
    parser.parse_args(namespace=c)

    username = os.getenv("DJANGO_USERNAME")
    api_key = os.getenv("DJANGO_API_KEY")
    c.get(username, api_key)
