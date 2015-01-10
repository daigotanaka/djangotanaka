from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import Page
from core.rutils import is_rmarkdown, rmarkdown_page
from core.utils import is_markdown, markdown_page


@receiver(post_save, sender=Page, dispatch_uid="update_page_content_cache")
def update_page_content_cache(sender, **kwargs):
    page = kwargs["instance"]
    if is_markdown(page.body):
        # It should not use page_id as a kwarg to keep the cache key consistent
        markdown_page(page.id, clear_cache=True)

    elif is_rmarkdown(page.body):
        # It should not use page_id as a kwarg to keep the cache key consistent
        rmarkdown_page(page.id, clear_cache=True)
