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

# # gc.enable()

# #spi
# SPI_SCLK= board.IO5
# SPI_MOSI= board.IO4
# # SPI_MISO= board.IO15


# #display
# LCD_CS = board.IO9
# LCD_DC = board.IO38
# LCD_RST = board.IO10
# LCD_BL = board.IO37


# # key
# KEY1= board.IO11
# KEY2= board.IO0
# KEY3= board.IO39

# # battery
# BATT = board.IO7



# #I2C DEVICES
# I2C_SCL = board.IO36
# I2C_SDA = board.IO35

# IOX = board.IO1


# # i2s
# AUDIO_SD = board.IO12
# AUDIO_DATA = board.IO13
# AUDIO_BCK = board.IO14
# AUDIO_WS = board.IO15

# def execfile(pyfile='code.py'):
#     supervisor.set_next_code_file(pyfile)
#     print("\033[2J",end="") #clear screen
#     print("Free memory:"+str(gc.mem_free()))
#     print("Next boot set to:")
#     print(pyfile)
#     try:
        
#         gc.collect()
#         exec(open(pyfile).read())
#     except Exception as err:
#         print(err)
#     print("Program finished ...")
#     print("\033[2J",end="") #clear screen



# displayio.release_displays()

# spi = busio.SPI(SPI_SCLK,SPI_MOSI)

# while not spi.try_lock():
#     pass
# spi.configure(baudrate=24000000) # Configure SPI for 24MHz
# spi.unlock()




# i2c = busio.I2C(I2C_SCL,I2C_SDA, frequency=100000,timeout=255)

# while not i2c.try_lock():
#     pass 
# i2c.unlock()



# # i2s = audiobusio.I2SOut(AUDIO_BCK,AUDIO_WS,AUDIO_DATA)
 


# # audio power,Pull SD_MODE low to place the device in shutdown
# audiopwr = digitalio.DigitalInOut(AUDIO_SD)
# audiopwr.direction = digitalio.Direction.OUTPUT
# audiopwr.value = False   #power on




# display_bus = FourWire(spi,command=LCD_DC,chip_select=LCD_CS) 

# lcd_reset = digitalio.DigitalInOut(LCD_RST)
# lcd_reset.direction = digitalio.Direction.OUTPUT

 
# def audiopwr_on():
#     audiopwr.value = True
    
# def audiopwr_off():
#     audiopwr.value = False    

# def disp_reset():
#     lcd_reset.value = True   #power on
#     time.sleep(0.1)
#     lcd_reset.value = False   #power off
#     time.sleep(0.1)
#     lcd_reset.value = True   #power on
#     time.sleep(0.1)

# disp_reset()

# display = ST7735R(display_bus, rotation=0, width=128, height=128, colstart=0,  backlight_pin=LCD_BL ,backlight_on_high = True , bgr=True)

# # display.bus.send(0x36, struct.pack(">h", 0xc8))
# display.root_group = None
# # display.root_group[0].hidden = False
# # display.root_group[1].hidden = True # logo
# # display.root_group[2].hidden = True # status bar

# imu = LSM6DS3TRC(i2c)

# keys = keypad.Keys((KEY1,KEY2,KEY3,), value_when_pressed=False, pull = True)
# # Clear any queued key transition events. Also sets overflowed to False.
# def clearkey():
#     keys.events.clear()
    
# # Create an event we will reuse over and over.
# event = keypad.Event()

# def getkey():     
#     if keys.events.get_into(event):
#         if event.pressed:
#             # print(event)
#             return event.key_number
        
#         if event.released:
#             return event.key_number+10
#             # print(event)
#             pass
#     return -1



