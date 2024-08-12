'''
fist.py
ICON from https://icons8.com/
v0.2.0
    20240612
    ported to cpy 9.x
v0.1.0
    20230801
    first release
    
'''




from magiclick import MagiClick
import terminalio,displayio,time,gc
import supervisor
import os
from adafruit_display_shapes.rect import Rect
from adafruit_display_text import label
import adafruit_imageload
import gifio
import struct

from random import randint
import audiocore
import array
import math

mc = MagiClick()
# Generate one period of sine wav, 8ksps 440 Hz sin wave:
length = 8000 // 1024
sine_wave = array.array("h", [0] * length)
for i in range(length):
    sine_wave[i] = int(math.sin(math.pi * 2 * i / length) * (2 ** 15))
sine_wave = audiocore.RawSample(sine_wave)

def playwave():
    mc.audio_enable()
     
    mc.audio.play(sine_wave, loop=True)
    time.sleep(0.1)
    mc.audio.stop()
    
    mc.audio_disable()
    pass




 
odg = gifio.OnDiskGif('images/fist/icons8-fist.gif')
print(odg.frame_count)
start = time.monotonic()
next_delay = odg.next_frame() # Load the first frame
end = time.monotonic()
overhead = end - start
#  
# print(overhead)

# odg.palette.make_transparent(0)
face = displayio.TileGrid(
    odg.bitmap,
    pixel_shader=displayio.ColorConverter(input_colorspace=displayio.Colorspace.RGB565_SWAPPED),
    x=8,
    y=8
    )


splash = displayio.Group(scale=2)
rect = Rect(0, 0, 64, 64, fill=0xffffff)
splash.append(rect)

splash.append(face)
mc.display.root_group =splash
mc.display.refresh()


gif_files=['icons8-fist.gif','icons8-fist (1).gif','icons8-fist (2).gif']
index=0


def draw_gif(filename):
    splash.pop()
    odg = gifio.OnDiskGif('images/fist/'+filename)
    cnt =odg.frame_count-6
    print(odg.frame_count)
    start = time.monotonic()
    next_delay = odg.next_frame() # Load the first frame
    end = time.monotonic()
    overhead = end - start
     
    print(overhead)

    # odg.palette.make_transparent(0)
    face = displayio.TileGrid(
        odg.bitmap,
        pixel_shader=displayio.ColorConverter(input_colorspace=displayio.Colorspace.RGB565_SWAPPED),
        x=8,
        y=8
        )
    splash.append(face)
    while cnt:
        time.sleep(max(0, next_delay - overhead))
        next_delay = odg.next_frame()
        cnt-=1
    
 

key = -1
mc.display.brightness=1.0
# Display repeatedly.
while True:
    acceleration = mc.imu.acceleration
    if acceleration[2] > 8.0:
        mc.exit()
        
    
    key_event = mc.keys.events.get()
    if key_event:
        if key_event.pressed:
            key = key_event.key_number
    else:
         key=-1
         
    if key==0:
        key=-1
        index=randint(0,2)
        
        draw_gif(gif_files[index])
        playwave()
        gc.collect()
        print(gc.mem_free())
    elif key==2:
        mc.exit()
    time.sleep(0.2)
 

