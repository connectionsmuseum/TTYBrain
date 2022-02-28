from email.policy import default
from time import sleep
from serial import Serial
from sources import NewsSource
from sources import ArtSource
from sources import WeatherSource
from sources import TutorialSource
from dial import Dial
from decouple import config
from signal import pause


class TeletypeController:
    _serial: Serial = None
    _tty_baud = 0
    _dial: Dial = None
    _sources = [TutorialSource(), NewsSource(), WeatherSource(), ArtSource()]
    _source_idx = 0
    _source_changed = True
    _break = False
    _dialing = False

    def dial_begin(self):
        self._dialing = True
        self._break = True
        self.print("\n\n", override=True)

    def dial_end(self, digit):
        self._dialing = False
        print(digit)
        self._source_idx = min(digit, len(self._sources) - 1)
        self._source_changed = True

    @property
    def current_source(self):
        return self._sources[self._source_idx]

    def __init__(self):
        self._serial = Serial(
            config("SERIAL_PORT", default="/dev/ttyACM0"),
            config("SERIAL_BAUD", default=9600),
        )
        self._tty_baud = config("TTY_BAUD", default=45)
        self._dial = Dial(
            config("DIAL_TRIGGER", default="GPIO2"),
            config("DIAL_PULSE", default="GPIO3"),
        )
        self._dial.dial_begin = lambda: self.dial_begin()
        self._dial.dial_end = lambda n: self.dial_end(n)

        # tutorial
        self._sources[0].ttyc = self

    def print(self, text: str, override=False):
        for char in text:
            if self._break and not override:
                self._break = False
                return
            c = str(char).replace("'", '"').replace("_", "-").replace("|", "!")
            self._serial.write(c.encode("ascii"))
            if c == "\r" or c == "\n":
                sleep(4 / self._tty_baud)
            else:
                sleep(1 / self._tty_baud)

    def begin(self):
        while True:
            if self._dial.dialing:
                continue
            text = self.current_source.update(
                ttyc=self, src_changed=self._source_changed
            )
            self._source_changed = False
            self.print(text)
            if self._source_idx == 0:
                for i in range(10):
                    if self._source_changed:
                        break
                    sleep(1)


if __name__ == "__main__":
    ttyc = TeletypeController()
    ttyc.begin()
    pause()
