import datetime
import inspect
import simplejson
import sys

from django.utils.timezone import utc

import core
# from core.models import Log


def execute_command(command):
    if not (command.name or command.raw_command):
        return "", ""

    if not command.name:
        command.name, data = interpret_command(command.raw_command)
        command_data = simplejson.loads(command.data)
        command_data.update(data)
        command.data = simplejson.dumps(command_data)

    if command.name and all_commands.get(command.name):
        return all_commands[command.name](command)

    return "", ""

def interpret_command(raw_command):
    """Interpret command from a free text input"""
    return None, {} # To be implemented


def beacon(command):
    data = simplejson.loads(command.data)
    now = datetime.datetime.utcnow().replace(tzinfo=utc)
    lat = data.get("lat")
    lng = data.get("lng")

    # Record in Log
    last_log = core.models.Log.objects.filter(created_by=command.created_by
        ).order_by("-created_at")
    if (not last_log or
            now - last_log[0].created_at > datetime.timedelta(hours=1)):
        core.models.Log.objects.create(
            created_by=command.created_by,
            lat=lat,
            lng=lng,
            raw_data= simplejson.dumps(data)
        )
    # TODO(Daigo): Insert code to trigger events

    # Just respond OK if no events are found
    response = {}
    response["status"] = "ok"
    return ("beacon", response)


# Register commands
all_commands = {}
for name, obj in inspect.getmembers(sys.modules[__name__]):
    if (inspect.isfunction(obj) and
            not name in ["execute_command", "interpret_command"]):
        all_commands[name] = obj
