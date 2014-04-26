
def execute_command(command, data):

    lat = None
    lng = None
    if type(data) is dict:
        lat = data.get("lat")
        lng = data.get("lng")

    response = {}
    response["status"] = "ok"

    return ("", response)
