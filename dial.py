from gpiozero import Button
from signal import pause
import time


class Dial:
    num = 0
    _count = 0
    _trigger = None
    _dial = None
    _dialing = False
    dial_begin = None
    dial_end = None

    __t = None

    @property
    def dialing(self):
        return self._dialing

    def _trigger_down(self):
        self._dialing = False
        self.num = self._count
        # print("T: v")
        # print(self.num)
        if callable(self.dial_end):
            self.dial_end(self.num)

    def _trigger_up(self):
        self._count = 0
        self._dialing = True
        # print("T: ^")
        if callable(self.dial_begin):
            self.dial_begin()

    def _dial_down(self):
        self._count += 1
        # print("pulse")
        # print(f"D: v | {time.time_ns() - self.__t}us")
        time.sleep(0.001)
        pass

    def _dial_up(self):
        # self._count += 1
        self.__t = time.time_ns()
        # print("D: ^")
        pass

    def __init__(self, trigger_pin, dial_pin, dial_begin=None, dial_end=None):
        self._trigger = Button(trigger_pin)
        self._dial = Button(dial_pin)

        self._trigger.when_pressed = lambda: self._trigger_down()
        self._trigger.when_released = lambda: self._trigger_up()
        self._dial.when_pressed = lambda: self._dial_down()
        self._dial.when_released = lambda: self._dial_up()
        # self._dial_begin = dial_begin
        # self._dial_end = dial_end


if __name__ == "__main__":
    dialer = Dial("GPIO2", "GPIO3")
    pause()
