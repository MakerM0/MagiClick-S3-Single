from magiclick import MagiClick
import os
import json
import random
import board
import time
import digitalio
import analogio
import displayio
import terminalio
import audiocore
import audiobusio
import gc
 
from adafruit_display_text import label, wrap_text_to_pixels, wrap_text_to_lines
gc.collect()
 

from adafruit_bitmap_font import bitmap_font
from displayio import Bitmap


mc = MagiClick()

# fontFile = "fonts/Fontquan-XinYiGuanHeiTi-Regular.pcf"
fontFile = "fonts/zhoufangrimingxie-10.pcf"

font = bitmap_font.load_font(fontFile, Bitmap)
# print(font.get_glyph(ord("1")))

asnsers=[]
with open('answersbook/answersbook.json','r') as jsonfile:
    content = jsonfile.read()
    answers= json.loads(content) 



# First set some parameters used for shapes and text
BORDER = 20
FONTSCALE = 1
BACKGROUND_COLOR = 0x00FF00  # Bright Green
FOREGROUND_COLOR = 0xAA0088  # Purple
TEXT_COLOR = 0xFFFF00
 
WRAP_WIDTH = 128//FONTSCALE



# Make the display context
splash = displayio.Group()
mc.display.root_group = splash



# Draw a label
text = "答\n案\n之\n书"
text_area = label.Label(font, text=text, color=TEXT_COLOR,scale=FONTSCALE)
text_area.color = (random.randint(10,255),random.randint(10,255),random.randint(10,255))
text_area.anchor_point = (0.5, 0.5)
text_area.anchored_position = (mc.display.width//2, mc.display.height//2)
text_area.line_spacing = 0.8
splash.append(text_area)

# display.brightness=1.0
 
gc.collect() 
 
ITEMS_NUM = len(answers)
# print(ITEMS_NUM) 
trig=False
mc.display.brightness=1.0
while True: 
     
    key_event = mc.keys.events.get()
    if key_event:
        if key_event.pressed:
            key = key_event.key_number
    else:
         key=-1
    
    if key==0:            
        key=-1 
        trig=False
        text = answers[f'{random.randint(0,ITEMS_NUM)+1}']['answer']
#         print(text)
        text = "\n".join(wrap_text_to_pixels(text, WRAP_WIDTH, font))
#         print(text)
        text = text.replace('-','')
#         print(text) 
        text_area.text = text
        text_area.color = (random.randint(10,255),random.randint(10,255),random.randint(10,255))
#         play_wave("system_power_on.wav")
        time.sleep(1)
        
    acceleration = mc.imu.acceleration
    if acceleration[2] > 8.0:
        mc.exit()
    
    time.sleep(0.05)


