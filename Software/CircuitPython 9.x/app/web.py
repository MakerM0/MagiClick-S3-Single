 
import time
import board,supervisor
import digitalio,displayio,terminalio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_display_text import label, wrap_text_to_pixels, wrap_text_to_lines
from magiclick import MagiClick


 

  

htmls=(

    ('https://space.bilibili.com/204526879','B站',None),
    
    ('https://oshwhub.com/kakaka/','立创开源平台',None),
    ('https://www.szlcsc.com/','立创商城',None),
    
    ('https://shop113593007.taobao.com/','乐鑫淘宝',None),
    ('https://oled-zjy.taobao.com/','中景园淘宝',None),
    ('https://anxinke.taobao.com/','安信可淘宝',None),
    )

from adafruit_bitmap_font import bitmap_font
from displayio import Bitmap

WRAP_WIDTH = 64

mc = MagiClick()
mc.display.brightness=1.0 
# fontFile = "fonts/Fontquan-XinYiGuanHeiTi-Regular.pcf"
fontFile = "fonts/wenquanyi_13px.pcf"

font = bitmap_font.load_font(fontFile, Bitmap)

label = label.Label(font, text='', color=0x2ad5ff,background_color=0x0,scale=2)



''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
mc.display.root_group = displayio.CIRCUITPYTHON_TERMINAL
trytime=0 
while not supervisor.runtime.usb_connected:    
    print("""
No USB connected
Please insert USB


    """)
    print(5-trytime)
    time.sleep(1.0)
    trytime+=1
    if trytime>=5:
        mc.exit()

# Define the keyboard object
keyboard = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(keyboard)

# Open the webpage
def openweb(html):
    if not isinstance(html, str):
        raise TypeError("Parameter must be of type int")     
    keyboard.press(Keycode.CONTROL, Keycode.T)
    keyboard.release_all()
    keyboard.press(Keycode.CONTROL, Keycode.L)
    keyboard.release_all()
    layout.write(html)
    keyboard.press(Keycode.ENTER)
    keyboard.release_all()
    keyboard.press(Keycode.ENTER)
    keyboard.release_all()

def draw(title:str):
    label.text = title
    print(title)
    
    
def main():
    # Define the key to simulate
    key = Keycode.F1
    # Simulate key press
    keyboard.press(key)
    keyboard.release(key)
    # Wait for the browser to open
    time.sleep(1)
    
    index=0
    LEN = len(htmls)
    
    
    label.anchor_point = (0.5, 0.5)
    label.anchored_position = (64,64)
    label.text = htmls[index][1]
    
    group=displayio.Group(scale=1)
    group.append(label)
    mc.display.root_group =group
    
    
    while True:
        time.sleep(0.1)
        
        acceleration = mc.imu.acceleration
        if acceleration[2] > 8.0:                
            mc.exit()
            
        key_event = mc.keys.events.get()
        if key_event:
            if key_event.released:
                key = key_event.key_number
        else:
             key=-1
        
        if key==0:
            openweb(htmls[index][0])
            
        if acceleration[0] <-3.0:
            index +=1
            if index==LEN:
                index=0
            
            draw(htmls[index][1])
            time.sleep(0.5)
            
            
            
        if acceleration[0] >3.0:
            index -=1
            if index<0:
                index=LEN-1
            text = "\n".join(wrap_text_to_pixels(htmls[index][1], WRAP_WIDTH, font))
            text = text.replace('-','')
            draw(text)
            time.sleep(0.5)
        
        
main()        
