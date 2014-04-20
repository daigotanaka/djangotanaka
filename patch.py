import os
import requests
import simplejson

from site_info import WEBSITE_URL

API_URL = WEBSITE_URL + "/api/v1"


class Command(object):
    def patch(self, username, api_key):
        filename = self.filenames[0]
        if not os.path.exists(filename):
            return
        with open(filename) as f:
            body = f.read()
        _, name = os.path.split(filename)
        pos = name.find(".")
        current_slug = name[0:pos] if pos > 0 else filename

        params = {
            "username": username,
            "api_key": api_key,
        }
        data = {
            "slug": self.new_slug,
            "body": body,
            "title": self.title,
            "status": self.status,
        }

        headers = {"content-type": "application/json"}
        # response = requests.patch(API_URL + "/page/", params=params, data=data)
        response = requests.patch(
                API_URL + "/page/" + current_slug + "/",
                headers=headers,
                params=params,
                data=simplejson.dumps(data)
            )
        print response


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Patch update an existing page")
    parser.add_argument("filenames", metavar="filename", type=str, nargs=1,
                           help="File name that matches the slug of the exiting article")
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
        "--new-slug",
        dest="new_slug",
        action="store",
        default=None,
        help="Store the slug to be updated"
    )

    c = Command()
    parser.parse_args(namespace=c)

    username = os.getenv("DJANGO_USERNAME")
    api_key = os.getenv("DJANGO_API_KEY")
    c.patch(username, api_key)
