import microcontroller
import displayio,os,terminalio
from magiclick import MagiClick
from adafruit_display_text import label
import time

mc = MagiClick()

def updateUF2(): 
    microcontroller.on_next_reset(microcontroller.RunMode.UF2)
    microcontroller.reset()
    
 
    
# left key
note = label.Label(font = terminalio.FONT,text = "  [ Update CPY ] \n\n\n  Left btn -> OK\nMiddle btn -> Quit", color = 0xF0f0FF,scale =1)

note.anchor_point = (0.5, 0)
note.anchored_position = (mc.display.width//2, 0)

curVersion =label.Label(font =terminalio.FONT, text = 'current version\n'+os.uname().version, color = 0x0ff00F,scale =1)
curVersion.anchor_point = (0.5, 1.0)
curVersion.anchored_position = (mc.display.width//2, mc.display.height)

group = displayio.Group()

group.append(note)
group.append(curVersion)

mc.display.root_group = group


mc.display.brightness=1.0


while True :
    time.sleep(0.1)
    key_event = mc.keys.events.get()
    if key_event:
        if key_event.pressed:
            key = key_event.key_number
    else:
         key=-1
         
    if key==1:
        updateUF2()
    if key==0:
        mc.exit()
        
        
