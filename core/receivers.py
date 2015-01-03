from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import Page
from core.rutils import is_rmarkdown, rmarkdown_page


@receiver(post_save, sender=Page, dispatch_uid="update_rmarkdown_cache")
def update_rmarkdown_cache(sender, **kwargs):
    page = kwargs['instance']
    if not is_rmarkdown(page.body):
        return
    # It should not use page_id as a kwarg to keep the cache key consistent
    rmarkdown_page(page.id, clear_cache=True)
