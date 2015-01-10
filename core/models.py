import datetime
import simplejson

from django.contrib.auth.models import User
from django.db.models import Model
from django.db.models import (CharField, DateTimeField, FloatField, ForeignKey,
                              TextField)

from core.commands import execute_command


STATUS_CHOICES = (
    ("private", "private"),
    ("public", "public")
)


class Command(Model):
    created_by = ForeignKey(User, related_name="created_commands")
    created_at = DateTimeField(auto_now=True)
    lat = FloatField(null=True)
    lng = FloatField(null=True)
    raw_command = TextField(blank=True)
    name = CharField(blank=True, max_length=256)
    data = CharField(blank=True, max_length=1024)
    response = TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.data:
            self.data = "{}"
        if type(self.data) == dict:
            self.data = simplejson.dumps(self.data)
        self.name, self.response = execute_command(self)
        super(Command, self).save(*args, **kwargs)


class Log(Model):
    created_by = ForeignKey(User, related_name="created_logs")
    created_at = DateTimeField(auto_now=True)
    lat = FloatField(null=True)
    lng = FloatField(null=True)
    raw_data = TextField(blank=True)


class Page(Model):
    created_by = ForeignKey(User, related_name="created_pages")
    created_at = DateTimeField()
    modified_at = DateTimeField(editable=False)
    status = CharField(
        max_length=16, choices=STATUS_CHOICES, default="private")
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


# Import receivers at the bottom to avoid circular imports
import receivers  # NOQA
