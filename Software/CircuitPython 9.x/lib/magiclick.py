import board
import time
import digitalio
import analogio
import gc
import os
import busio
import audiobusio
import audiocore
import terminalio
import keypad
import neopixel
import displayio
import struct
import microcontroller
import supervisor 
from microcontroller import nvm

from adafruit_lsm6ds.lsm6ds3trc import LSM6DS3TRC

try:
    # Only used for typing
    from typing import Tuple, Optional, Union, Iterator
    from neopixel import NeoPixel
    from keypad import Keys
    import adafruit_hid  # pylint:disable=ungrouped-imports
except ImportError:
    pass


__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/MakerM0/MagiClick-S3-Single.git"


class ParaAddr:
        COUNTER_NEW = 0
        FLAPPY_HIGHSCORE = 4
        
class MagiClick:
    def __init__(self) -> None:

        # led
        self._pixels = neopixel.NeoPixel(board.NEOPIXEL,1,auto_write=False)

         # Define display:        
        self.display = board.DISPLAY
        self.display.brightness=0.0

        #Define key
        KEY1= board.IO11
        KEY2= board.IO0
        KEY3= board.IO39
         
        self._keys = keypad.Keys((KEY1,KEY2,KEY3), value_when_pressed=False, pull=True)

        #define Battery
        self._batt= analogio.AnalogIn(board.BAT)

        #define imu
        I2C_SCL = board.IO36
        I2C_SDA = board.IO35
        i2c = busio.I2C(I2C_SCL,I2C_SDA, frequency=400000,timeout=255)

        while not i2c.try_lock():
            pass 
        i2c.unlock()
        self.imu = LSM6DS3TRC(i2c)
        
        #Define Speaker
        AUDIO_SD = board.IO12
        AUDIO_DATA = board.IO13
        AUDIO_BCK = board.IO14
        AUDIO_WS = board.IO15
        self._speaker_enable = digitalio.DigitalInOut(AUDIO_SD)
        self._speaker_enable.switch_to_output(value=False)
        self.audio = audiobusio.I2SOut(AUDIO_BCK,AUDIO_WS,AUDIO_DATA)

        self._ledpwr = digitalio.DigitalInOut(board.IO16)
        self._ledpwr.direction = digitalio.Direction.OUTPUT
        self._ledpwr.value = False


    def led_on(self):
        self._ledpwr.value = True

    def led_off(self):
        self._ledpwr.value = False

    def write_para(self,addr,data:int):
        if self.read_para(addr) == data:
            return 
        nvm[addr:addr+4]=data.to_bytes(4,'little')
        
         
    
    def read_para(self,addr) -> int:
        data = nvm[addr:addr+4]
        return (int.from_bytes(data,'little'))

    def audio_enable(self):
        self._speaker_enable.value=True
    
    def audio_disable(self):
        self._speaker_enable.value=False

    def get_batt(self) -> int:
        return int((self._batt.value * 3300) / 65535 *2)
    
    @property
    def pixels(self):
        return self._pixels
        
    @property
    def keys(self) -> Keys:
        """
        The keys on the MagiClick. Uses events to track key number and state, e.g. pressed or
        released. You must fetch the events using ``keys.events.get()`` and then the events are
        available for usage in your code. Each event has three properties:

        * ``key_number``: the number of the key that changed. Keys are numbered starting at 0.
        * ``pressed``: ``True`` if the event is a transition from released to pressed.
        * ``released``: ``True`` if the event is a transition from pressed to released.

        ``released`` is always the opposite of ``pressed``; it's provided for convenience
        and clarity, in case you want to test for key-release events explicitly.

        The following example prints the key press and release events to the serial console.

        .. code-block:: python

            from magiclick import MagiClick

            mc = MagiClick()

            while True:
                key_event = mc.keys.events.get()
                if key_event:
                    print(key_event)
        """
        return self._keys

    def exit(self):
        self.display.brightness=0.0
        supervisor.set_next_code_file("code.py")
        supervisor.reload()
