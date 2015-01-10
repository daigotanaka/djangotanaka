import imp
import json
import logging
import re
import requests

from core.models import Page
from libs.utils import cache_for

logger = logging.getLogger(__name__)


def is_rmarkdown(content):
    # TODO(Daigo): Better header pattern?
    markdown_header = "---"
    if (content[0:len(markdown_header)] == markdown_header or
            re.match(r"http[s]:\/\/.*\.Rmd$", content)):
        return True
    return False


@cache_for(60 * 60 * 24 * 30)
def rmarkdown_page(page_id, **kwargs):
    page = Page.objects.get(id=page_id)

    if re.match(r"http[s]:\/\/.*\.Rmd$", page.body):
        response = requests.get(page.body)
        body = response.content
    else:
        body = page.body

    if page.variables:
        try:
            variables = json.loads(page.variables)
            body = body % variables
            logger.info(variables)
        except Exception, err:
            logger.info(err)
            pass

    if not RPY2_INSTALLED:
        logger.info("rpy2 not found. I won't convert the raw text.")
        return body
    with open("/var/tmp/tmp.Rmd", "w") as f:
        f.write(body)
    ro.r("library('knitr');"
         "knit2html(input='/var/tmp/tmp.Rmd', output='/var/tmp/tmp.html');")
    with open("/var/tmp/tmp.html", "r") as f:
        content = f.read()
    content = re.sub(r"<[/]*body>", "", content)
    content = re.sub(r"<[/]*html>", "", content)
    content = content[content.find("</head>") + len("</head>"):]
    return content


# Import only if rpy2 is available
try:
    imp.find_module("rpy2")
    from rpy2 import robjects as ro
    RPY2_INSTALLED = True
except ImportError:
    RPY2_INSTALLED = False
