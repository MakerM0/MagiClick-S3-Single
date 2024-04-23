# SPDX-FileCopyrightText: 2019 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`nv3023`
====================================================

Displayio driver for ST7789 based displays.

* Author(s): Melissa LeBlanc-Williams

Implementation Notes
--------------------

**Hardware:**

* Adafruit 1.3" 240x240 Wide Angle TFT LCD Display with MicroSD - ST7789:
  https://www.adafruit.com/product/4313

* Adafruit 1.54" 240x240 Wide Angle TFT LCD Display with MicroSD - ST7789:
  https://www.adafruit.com/product/3787

* Adafruit 1.14" 240x135 Color TFT Display + MicroSD Card Breakout - ST7789:
  https://www.adafruit.com/product/4383

* Adafruit Mini PiTFT 1.3" - 240x240 TFT Add-on for Raspberry Pi:
  https://www.adafruit.com/product/4484

* Adafruit 1.3" Color TFT Bonnet for Raspberry Pi - 240x240 TFT + Joystick Add-on
  https://www.adafruit.com/product/4506

* Adafruit Mini PiTFT - 135x240 Color TFT Add-on for Raspberry Pi:
  https://www.adafruit.com/product/4393

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

"""

# Starting in CircuitPython 9.x fourwire will be a seperate internal library
# rather than a component of the displayio library
try:
    from fourwire import FourWire
    from busdisplay import BusDisplay
except ImportError:
    from displayio import FourWire
    from displayio import Display as BusDisplay

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_ST7789.git"

_INIT_SEQUENCE = (
    b"\x01\x80\x96"  # _SWRESET and Delay 150ms
    b"\xff\x01\xa5"
    b"\x3E\x01\x09"
    b"\x3A\x01\x65"
    b"\x82\x01\x00"
    b"\x98\x01\x00"
    b"\x63\x01\x0f"
    b"\x64\x01\x0f"
    b"\xB4\x01\x34"
    b"\xB5\x01\x30"
    b"\x83\x01\x03"
    b"\x86\x01\x04"
    b"\x87\x01\x16"
    b"\x88\x01\x0A"
    b"\x89\x01\x27"  
    b"\x93\x01\x63"
    b"\x96\x01\x81" 
    b"\xC3\x01\x10"
    b"\xE6\x01\x00"
    b"\x99\x01\x01"
    b"\x70\x01\x09" # VRP 31 1
    b"\x71\x01\x1D" # VRP 30 3
    b"\x72\x01\x14" # VRP 29 7
    b"\x73\x01\x0a" # VRP 28 9
    b"\x74\x01\x11" # VRP 25 11
    b"\x75\x01\x16" # VRP 23 13
    b"\x76\x01\x38" # VRP 21 5
    b"\x77\x01\x0B" # VRP 17 15
    b"\x78\x01\x08" # VRP 14 16
    b"\x79\x01\x3E" # VRP 10 6
    b"\x7a\x01\x07" # VRP 8 14
    b"\x7b\x01\x0D" # VRP 6 12
    b"\x7c\x01\x16" # VRP 3 10
    b"\x7d\x01\x0F" # VRP 2 8
    b"\x7e\x01\x14" # VRP 1 4
    b"\x7f\x01\x05" # VRP 0 2
    b"\xa0\x01\x04" # VRN 31 1
    b"\xa1\x01\x28" # VRN 30 3
    b"\xa2\x01\x0c" # VRN 29 7
    b"\xa3\x01\x11" # VRN 28 9
    b"\xa4\x01\x0b" # VRN 25 11
    b"\xa5\x01\x23" # VRN 23 13
    b"\xa6\x01\x45" # VRN 21 5
    b"\xa7\x01\x07" # VRN 17 15
    b"\xa8\x01\x0a" # VRN 14 16
    b"\xa9\x01\x3b" # VRN 10 6
    b"\xaa\x01\x0d" # VRN 8 14
    b"\xab\x01\x18" # VRN 6 12
    b"\xac\x01\x14" # VRN 3 10
    b"\xad\x01\x0F" # VRN 2 8
    b"\xae\x01\x19" # VRN 1 4
    b"\xaf\x01\x08" # VRN 0 2
    b"\xff\x01\x00"
    b"\x11\x80\xFF"  # _SLPOUT and Delay 500ms
    b"\x36\x01\x88"
    b"\x29\x80\xFF"  # _DISPON and Delay 500ms
 
)


# pylint: disable=too-few-public-methods
class NV3023(BusDisplay):
    """NV3023 driver"""

    def __init__(self, bus: FourWire, **kwargs) -> None:
        super().__init__(bus, _INIT_SEQUENCE, **kwargs)
