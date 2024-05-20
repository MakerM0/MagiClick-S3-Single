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
from magiclick import *
from adafruit_display_text import label, wrap_text_to_pixels, wrap_text_to_lines
gc.collect()
# display.brightness=0.0

from adafruit_bitmap_font import bitmap_font
from displayio import Bitmap

# fontFile = "fonts/Fontquan-XinYiGuanHeiTi-Regular.pcf"
fontFile = "fonts/wenquanyi_13px.pcf"

font = bitmap_font.load_font(fontFile, Bitmap)
# print(font.get_glyph(ord("1")))

asnsers=[]
with open('answersbook/answersbook.json','r') as jsonfile:
    content = jsonfile.read()
    answers= json.loads(content) 


# battery = analogio.AnalogIn(BATT)
# bat_raw = battery.value
# 
# random.seed(bat_raw)

 

# i2s = audiobusio.I2SOut(AUDIO_BCK,AUDIO_WS,AUDIO_DATA)
# def play_wave(filename):
#     global trig
#     print(filename)
#     audiopwr_on()    
#     
#     try :         
#         wave = audiocore.WaveFile('/audio/sys/{}'.format(filename))
#         i2s.play(wave)
#         while i2s.playing: 
#             pass
#     except Exception as e : 
#         print (e)
#  
#     audiopwr_off() 
#     gc.collect()
#     pass 



# First set some parameters used for shapes and text
BORDER = 20
FONTSCALE = 1
BACKGROUND_COLOR = 0x00FF00  # Bright Green
FOREGROUND_COLOR = 0xAA0088  # Purple
TEXT_COLOR = 0xFFFF00
 
WRAP_WIDTH = 128//FONTSCALE



# Make the display context
splash = displayio.Group()
display.root_group = splash



# Draw a label
text = "答\n案\n之\n书"
text_area = label.Label(font, text=text, color=TEXT_COLOR,scale=FONTSCALE)
text_area.color = (random.randint(10,255),random.randint(10,255),random.randint(10,255))
text_area.anchor_point = (0.5, 0.5)
text_area.anchored_position = (display.width//2, display.height//2)

splash.append(text_area)

# display.brightness=1.0
 
gc.collect() 
 
ITEMS_NUM = len(answers)
# print(ITEMS_NUM) 
trig=False 
while True: 
     
    key = getkey()
    
    if key==0:            
         
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
        
    acceleration = imu.acceleration
    if acceleration[2] > 8.0:
        returnMainPage()
    
    time.sleep(0.05)


