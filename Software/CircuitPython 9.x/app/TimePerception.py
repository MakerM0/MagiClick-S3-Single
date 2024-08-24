from magiclick import MagiClick


import os,displayio,supervisor,gc,terminalio
import rtc
import time
from adafruit_display_text import label
import board,microcontroller


mc = MagiClick()

from adafruit_bitmap_font import bitmap_font
font_file = "fonts/LeagueSpartan-Bold-16.bdf"
font = bitmap_font.load_font(font_file)
# font = terminalio.FONT


main_group = displayio.Group()
mc.display.root_group=main_group


t_label = label.Label(terminalio.FONT, color=0x2f88ff, scale=3)
t_label.anchor_point = (0.5, 0.5)
t_label.anchored_position = (mc.display.width//2, mc.display.height//2)
t_label.text = "Press"

main_group.append(t_label)

mc.display.auto_refresh=False
mc.display.refresh()
microcontroller.cpu.frequency=160000000

mc.display.brightness = 1.0
now = 0
while True:
    time.sleep(0.001)
    key_event = mc.keys.events.get()
    if key_event:
        if key_event.pressed:
            key = key_event.key_number
        elif key_event.released:
            key = key_event.key_number+10
        
    else:
         key=-1
         
    if key==0:
        now = time.monotonic()
        t_label.text="Timing"
        print("Timing")
        mc.display.refresh()
    elif key == 10:
        t = time.monotonic()-now
        t_label.text= f'{t:.3f}'
        print("end")
        print(t)
        mc.display.refresh()
        
    elif key==2:
        print('exit')
        microcontroller.cpu.frequency=240000000
        mc.exit()
        
    acceleration = mc.imu.acceleration
    if acceleration[2] > 8.0:
        mc.exit()
    


