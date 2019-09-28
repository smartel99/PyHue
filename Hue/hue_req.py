import requests
import json

from Hue import errors

api_url = "http://192.168.0.100/api"


def resp_has_errors(resp) -> bool:
    if type(resp) == list:
        resp = resp[0]

    for key in resp:
        if key == "error":
            return True


def check_resp(resp):
    if resp.status_code != 200:
        raise errors.HTTPException(resp.status_code)

    if type(resp.json()) == list:
        resp = resp.json()[0]
    else:
        resp = resp.json()

    if resp_has_errors(resp):
        raise errors.InvalidRequest(resp)


def create_username():
    req = {
        "devicetype": "hue_app#python"
    }
    resp = requests.post(api_url, json=req)

    check_resp(resp)

    with open("setup.ini", "w+") as setup_file:
        try:
            config = json.loads(setup_file.read())
        except json.decoder.JSONDecodeError:
            config = {}
        config["username"] = resp.json()[0]["success"]["username"]
        new_config = json.dumps(config, indent=True)
        setup_file.write(new_config)
    return resp.json()[0]["success"]["username"]


def get_username():
    try:
        with open("setup.ini", "r") as raw_setup:
            setup = json.loads(raw_setup.read())
            return setup["username"]
    except Exception:
        return create_username()


def get_lights(username: str) -> dict:
    url = "/".join([api_url, username, "lights"])
    resp = requests.get(url)

    check_resp(resp)

    lights = {}
    raw_lights = resp.json()

    if type(raw_lights) == list:
        raw_lights = raw_lights[0]

    for light in raw_lights:
        lights[raw_lights[light]["name"]] = {
            "productname": raw_lights[light]["productname"],
            "id": light,
            "type": raw_lights[light]["config"]["archetype"]
        }

    return lights


def set_light_state(username: str, light_id: str, on: bool, transitiontime=0):
    url = "/".join([api_url, username, "lights", light_id, "state"])
    body = {
        "on": on,
        "transitiontime": transitiontime
    }
    resp = requests.put(url, data=json.dumps(body))

    check_resp(resp)


def set_light_color(username, light_id, hsv, transitiontime=0):
    url = "/".join([api_url, username, "lights", light_id, "state"])
    body = {
        "hue": hsv["h"],
        "sat": hsv["s"],
        "bri": hsv["v"],
        "transitiontime": transitiontime
    }

    resp = requests.put(url, data=json.dumps(body))

    check_resp(resp)


def get_light_state(username, light_id) -> dict:
    url = "/".join([api_url, username, "lights", light_id])
    resp = requests.get(url)

    check_resp(resp)

    if type(resp.json()) == list:
        resp = resp.json()[0]
    else:
        resp = resp.json()

    return resp["state"]
