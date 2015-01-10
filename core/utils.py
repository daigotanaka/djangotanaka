import logging
import markdown2
import re
import requests

from core.models import Page
from libs.utils import cache_for

logger = logging.Logger(__name__)


def is_markdown(content):
    markdown_header = "<!--markdown"
    if (content[0:len(markdown_header)] == markdown_header or
            re.match(r"http[s]:\/\/.*\.md$", content)):
        return True
    return False


@cache_for(60 * 60 * 24 * 30)
def markdown_page(page_id, **kwargs):
    page = Page.objects.get(id=page_id)

    if re.match(r"http[s]:\/\/.*\.md$", page.body):
        response = requests.get(page.body)
        body = response.content
    else:
        body = page.body

    content = markdown2.markdown(
        body,
        extras=["code-friendly", "fenced-code-blocks", "footnotes",
                "tables"])
    return content
