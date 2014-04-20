import datetime

from django.contrib.auth.models import User
from django.db.models import Model
from django.db.models import CharField, DateTimeField, TextField


STATUS_CHOICES = (
    ("private", "private"),
    ("public", "public")
)

class Page(Model):
    created_at = DateTimeField()
    modified_at = DateTimeField(editable=False)
    status = CharField(max_length=16, choices=STATUS_CHOICES, default="private")
    title = CharField(blank=True, max_length=256)
    slug = CharField(blank=False, unique=True, max_length=256)
    head = TextField(blank=True)
    body = TextField(blank=True)
    foot = TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = datetime.datetime.now()
        self.modified_at = datetime.datetime.now()
        return super(Page, self).save(*args, **kwargs)
