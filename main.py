import time
import random

from Hue import hue


def main():
    h = hue.Hue()
    h.set_light_state("bedroom 1", True)
    h.set_light_state("bedroom 2", True)
    while True:
        h.set_light_hsv("bedroom 1", random.randint(0, 65536), random.randint(0, 254),
                        random.randint(0, 254))
        h.set_light_hsv("bedroom 2", random.randint(0, 65536), random.randint(0, 254),
                        random.randint(0, 254))
        time.sleep(0.1)


if __name__ == '__main__':
    main()
