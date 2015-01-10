import logging
import markdown2

from core.models import Page
from libs.utils import cache_for

logger = logging.Logger(__name__)


def is_markdown(content):
    markdown_header = "<!--markdown"
    if content[0:len(markdown_header)] == markdown_header:
        return True
    return False


@cache_for(60 * 60 * 24 * 30)
def markdown_page(page_id, **kwargs):
    page = Page.objects.get(id=page_id)
    content = markdown2.markdown(
        page.body,
        extras=["code-friendly", "fenced-code-blocks", "footnotes",
                "tables"])
    return content
