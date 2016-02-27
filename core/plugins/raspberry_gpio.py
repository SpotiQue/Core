from functools import wraps
from alsaaudio import Mixer
import RPi.GPIO as GPIO


def debounced(f):
    @wraps(f)
    def _wrapper(self, *args, **kwargs):
        if not self.is_pressed:
            self.is_pressed = True
            return f(self, *args, **kwargs)
    return _wrapper


class RaspberryGPIOPlugin:

    buttons = {
        12: "volume_up",
        11: "volume_down",
        8: "skip",
        10: "play_pause",
    }

    def __init__(self, player):
        self.player = player
        self._alsa_mixer = Mixer(control="PCM")
        self.is_pressed = False
        GPIO.setmode(GPIO.BOARD)
        input_buttons = [k for k in self.buttons.keys()]
        GPIO.setup(input_buttons, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def __call__(self):
        for port_number, callback_name in self.buttons.items():
            if GPIO.input(port_number) == 0:
                getattr(self, callback_name)()
                return
        else:
            self.is_pressed = False

    def _change_volume(self, change):
        new_volume = self.current_volume + change
        self._alsa_mixer.setvolume(new_volume)

    @property
    def current_volume(self):
        return self._alsa_mixer.getvolume()[0]

    @debounced
    def skip(self):
        self.player.skip()

    @debounced
    def play_pause(self):
        self.player.play_pause()

    def volume_up(self):
        self._change_volume(1)

    def volume_down(self):
        self._change_volume(-1)
