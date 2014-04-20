import os
import requests
import simplejson

from site_info import WEBSITE_URL

API_URL = WEBSITE_URL + "/api/v1"


class Command(object):

    def post(self, username, api_key):
        filename = self.filenames[0]
        if not os.path.exists(filename):
            return
        with open(filename) as f:
            body = f.read()
        _, name = os.path.split(filename)
        pos = name.find(".")
        slug = name[0:pos] if pos > 0 else filename

        params = {
            "username": username,
            "api_key": api_key,
        }
        data = {
            "slug": slug,
            "body": body,
            "title": self.title or slug,
            "status": self.status or "private",
        }

        headers = {"content-type": "application/json"}
        # response = requests.patch(API_URL + "/page/", params=params, data=data)
        response = requests.post(
                API_URL + "/page/",
                headers=headers,
                params=params,
                data=simplejson.dumps(data)
            )

        if response.status_code == 201:
            print ("Posted successfully at %s/%s" %
                (WEBSITE_URL, slug))
        else:
            print str(response.status_code) + ": Oops, something went wrong."


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Post a new page")
    parser.add_argument("filenames", metavar="filename", type=str, nargs=1,
        help="File name for the new page")
    parser.add_argument(
        "--title",
        dest="title",
        action="store",
        default=None,
        help="The title"
    )
    parser.add_argument(
        "--status",
        dest="status",
        action="store",
        default=None,
        help="The status (public|private)"
    )

    c = Command()
    parser.parse_args(namespace=c)

    username = os.getenv("DJANGO_USERNAME")
    api_key = os.getenv("DJANGO_API_KEY")
    c.post(username, api_key)
