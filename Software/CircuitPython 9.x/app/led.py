# SPDX-FileCopyrightText: 2021 Ruiz Brothers for Adafruit Industries
# SPDX-License-Identifier: MIT
# https://learn.adafruit.com/neopixel-ring-lamp/code

from magiclick import MagiClick
import board,displayio,digitalio
import neopixel
from adafruit_led_animation.animation.pulse import Pulse
from adafruit_led_animation.animation.rainbow import Rainbow
from adafruit_led_animation.animation.rainbowsparkle import RainbowSparkle
from adafruit_led_animation.animation.rainbowcomet import RainbowComet
from adafruit_led_animation.sequence import AnimationSequence
from adafruit_led_animation.color import PURPLE



# ledpwr = digitalio.DigitalInOut(board.NEOPIXEL_PWR)
# ledpwr.direction = digitalio.Direction.OUTPUT
# ledpwr.value = True

mc = MagiClick()
mc.display.brightness=1.0
mc.pixels.auto_write=True
# # Update this to match the number of NeoPixel LEDs connected to your board.
# num_pixels = 1
# 
# pixels = neopixel.NeoPixel(board.NEOPIXEL, num_pixels, auto_write=True)
# pixels.brightness = 0.5
mc.led_on()
rainbow = Rainbow(mc.pixels, speed=0.01, period=1)
rainbow_sparkle = RainbowSparkle(mc.pixels, speed=0.05, num_sparkles=15)
rainbow_comet = RainbowComet(mc.pixels, speed=.01, tail_length=20, bounce=True)
pulse = Pulse(mc.pixels, speed=.05, color=PURPLE, period=3)

animations = AnimationSequence(
    pulse,
    rainbow_sparkle,
    rainbow_comet,
    rainbow,
    advance_interval=5,
    auto_clear=True,
    random_order=False
)
mc.display.root_group = displayio.CIRCUITPYTHON_TERMINAL
print("""
pulse
rainbow_sparkle
rainbow_comet
rainbow
""")

while True:
    animations.animate()
    #exit 
    acceleration = mc.imu.acceleration
    if acceleration[2] > 8.0:
        mc.pixels.deinit()
        mc.exit()
    
    