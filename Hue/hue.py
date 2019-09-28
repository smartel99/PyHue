from Hue import hue_req, errors


class Hue:
    def __init__(self, ):
        self.username: str = hue_req.get_username()
        self.lights: dict = hue_req.get_lights(self.username)

    def set_light_state(self, light: str, on: bool, transitiontime=0):
        light_id = self.get_light_id_by_name(light)
        hue_req.set_light_state(self.username, light_id, on, transitiontime)

    def set_light_hsv(self, light: str, hue: int, sat: int, val: int, transitiontime=0):
        light_id = self.get_light_id_by_name(light)
        hsv = {
            "h": hue,
            "s": sat,
            "v": val
        }
        hue_req.set_light_color(self.username, light_id, hsv, transitiontime)

    def get_light_id_by_name(self, light: str) -> str:
        for l in self.lights:
            if light == l:
                return self.lights[light]["id"]
            elif self.lights[l]["id"] == light:
                return light
        raise errors.InvalidArgument("light", light)

    def get_light_state(self, light: str) -> dict:
        light_id = self.get_light_id_by_name(light)
        return hue_req.get_light_state(self.username, light_id)
