
def execute_command(command, data):

    lat = data.get("lat")
    lng = data.get("lng")
    if lat and lng:
        return (
                "",
                ("Your location is latitude %.2f and longitude %.2f" %
                    (float(lat), float(lng)))
                )

    response = {}
    response["status"] = "ok"

    return ("", response)
