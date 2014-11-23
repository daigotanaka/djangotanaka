import imp
import re

from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import Page
from libs.utils import cache_for

import logging
logger = logging.getLogger(__name__)


def is_rmarkdown(content):
    # TODO(Daigo): Better header pattern?
    markdown_header = "---"
    if content[0:len(markdown_header)] == markdown_header:
        return True
    return False


@cache_for(60 * 60 * 24 * 30)
def rmarkdown_page(page_id, **kwargs):
    page = Page.objects.get(id=page_id)
    if not RPY2_INSTALLED:
        return page.body
    with open("/var/tmp/tmp.Rmd", "w") as f:
        f.write(page.body)
    ro.r("library('knitr');"
         "knit2html(input='/var/tmp/tmp.Rmd', output='/var/tmp/tmp.html');")
    with open("/var/tmp/tmp.html", "r") as f:
        content = f.read()
    content = re.sub(r"<[/]*body>", "", content)
    content = re.sub(r"<[/]*html>", "", content)
    content = content[content.find("</head>"):]
    return content


@receiver(post_save, sender=Page, dispatch_uid="update_rmarkdown_cache")
def update_rmarkdown_cache(sender, **kwargs):
    page = kwargs['instance']
    if not is_rmarkdown(page.body):
        return
    rmarkdown_page(page_id=page.id, clear_cache=True)


# Import only if rpy2 is available
try:
    imp.find_module("rpy2")
    from rpy2 import robjects as ro
    RPY2_INSTALLED = True
except ImportError:
    RPY2_INSTALLED = False
