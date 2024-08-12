'''
v0.2.0
    add mac command+F3 进入桌面,未完成


'''
import time
import board
import digitalio,displayio,terminalio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_display_text import label, wrap_text_to_lines
from adafruit_bitmap_font import bitmap_font
import adafruit_imageload
from magiclick import MagiClick

import supervisor

mc = MagiClick()
mc.display.brightness=1.0
'''

The icons is from here  https://icons8.com/


Modify the keymap to implement more functionality

---------------------------------------------------------
| image | text | keycode1 | keycode2 | keycode3 | ..... |
---------------------------------------------------------

keycode
https://docs.circuitpython.org/projects/hid/en/latest/_modules/adafruit_hid/keycode.html

'''
MAC = False
# Choose the correct modifier key for Windows or Mac.
# Comment one line and uncomment the other.

if not MAC:    
    MODIFIER = Keycode.CONTROL  # For Windows
else:
    MODIFIER = Keycode.COMMAND  # For Mac

keymap=(
    ('desktop_96px.png','Desktop',Keycode.FN,Keycode.F11) if MAC else ('desktop_96px.png','Desktop',Keycode.GUI,Keycode.D),
    ('explorer_96px.png','explorer',Keycode.GUI,Keycode.E),
    ('system_96px.png','Taskmgr',MODIFIER,Keycode.SHIFT,Keycode.ESCAPE),
    (None,'Cut',MODIFIER,Keycode.X),
    (None,'Copy',MODIFIER,Keycode.C),
    (None,'Paste',MODIFIER,Keycode.V),    
    ('f5_96px_.png','F5',Keycode.F5),
        )

 
ICON_WIDTH=96
ICON_HEIGHT=96

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
trytime=0
mc.display.root_group = displayio.CIRCUITPYTHON_TERMINAL
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
        
     


LEN = len(keymap)
index=0

font =terminalio.FONT
# font = bitmap_font.load_font("fonts/LeagueSpartan-Bold-16.bdf")

mc.display.root_group=None
main_group = displayio.Group()
mc.display.root_group =main_group
# label 
keylabel = label.Label(font, color=0x00ff00, scale=4)
keylabel.anchor_point = (0.5, 0.5)
keylabel.anchored_position = (mc.display.width // 2, mc.display.height // 2)
keylabel.text = "" 


main_group.append(keylabel)


#image, 8bit png
transparent_img = displayio.Bitmap(ICON_WIDTH,ICON_HEIGHT,1)
palette = displayio.Palette(1)
palette[0]=0x000000
# Set the transparency index color to be hidden
palette.make_transparent(0)
tile_grid = displayio.TileGrid(transparent_img,pixel_shader = palette)
tile_grid.x = mc.display.width // 2 - tile_grid.tile_width // 2
tile_grid.y = mc.display.height // 2 - tile_grid.tile_height // 2 - 20

main_group.append(tile_grid)







def draw_img_or_text():
    if keymap[index][0] != None:
        try:
            image, palette = adafruit_imageload.load("/images/unikey/"+keymap[index][0])
            palette.make_transparent(0)
            tile_grid.bitmap = image
            tile_grid.pixel_shader = palette
            keylabel.scale=2
            keylabel.anchored_position = (mc.display.width // 2, 105)
            keylabel.text =keymap[index][1]
        except Exception as e:
            print (e)            
            pass
    else:
        tile_grid.bitmap = transparent_img
        keylabel.scale=4
        keylabel.anchored_position = (mc.display.width // 2,  mc.display.height // 2)
        keylabel.text = "\n".join(wrap_text_to_lines(keymap[index][1], 5))
        

draw_img_or_text()

mc.display.root_group =main_group



kbd = Keyboard(usb_hid.devices)


 
print(keymap)      
while True:
    key_event = mc.keys.events.get()
    if key_event:
        if key_event.pressed:
            key = key_event.key_number
    else:
         key=-1
    
    if key==0:
        key=-1
        kbd.send(*keymap[index][2:])

    
    
    acceleration = mc.imu.acceleration
    if acceleration[2] > 8.0:
        mc.exit()
    if acceleration[0] <-3.0:
        index -= 1
        if index<0:
            index=LEN-1 
        draw_img_or_text()
        time.sleep(0.5)
        pass
 
        
    if acceleration[0] >3.0:
        index += 1
        if index>=LEN:
            index=0 
        draw_img_or_text()
        time.sleep(0.5)
        pass     
 
    
    time.sleep(0.1)
    
    
    



