from magiclick import MagiClick
from adafruit_simple_text_display import SimpleTextDisplay
import time,os

import microcontroller
# print(microcontroller.cpu.frequency)
# print(microcontroller.cpu.temperature)

mc = MagiClick()
mc.display.brightness=0.0

def display_text(
    title: Optional[str] = None,
    title_scale: int = 2,
    title_length: int = 80,
    text_scale: int = 1,
    font: Optional[str] = None,
    ) -> SimpleTextDisplay:    
    return SimpleTextDisplay(
            title=title,
            title_color=SimpleTextDisplay.YELLOW,
            title_scale=title_scale,
            title_length=title_length,
            text_scale=text_scale,
            font=font,
            colors=(SimpleTextDisplay.GREEN,
                    SimpleTextDisplay.GREEN,
                    SimpleTextDisplay.GREEN,
                    SimpleTextDisplay.GREEN,
                    SimpleTextDisplay.GREEN,
                    SimpleTextDisplay.GREEN,
                    SimpleTextDisplay.GREEN,
                    SimpleTextDisplay.AQUA,),
            display=mc.display,
        )



text_lines = display_text(title=" Sys Info")

cpy = os.uname().version.split(' ',3)
# print (cpy)
# while True:
text_lines[0].text="CPY   : " + cpy[0]
text_lines[1].text="Build : " + cpy[2]
text_lines[2].text="CPU   : " + os.uname().sysname
text_lines[3].text="Freq  : " + str(microcontroller.cpu.frequency/1000000)+ 'MHz'
text_lines[4].text="Author: MakerM0" 
text_lines[5].text=os.uname().machine.split(' with ')[0] 
text_lines[7].text="Icons by Icons8" 
print (os.uname().machine )
 
text_lines.show()
mc.display.brightness=1.0
microcontroller.cpu.frequency = 80000000
time.sleep(1.0)
key=-1
while True:
    time.sleep(0.1)
    
    acceleration = mc.imu.acceleration
    if acceleration[2] > 8.0:
        mc.display.brightness=0.0
        microcontroller.cpu.frequency = 240000000
        mc.exit()
        
    
        
    key_event = mc.keys.events.get()
    if key_event:
        if key_event.pressed:
            mc.display.brightness=0.0
            microcontroller.cpu.frequency = 240000000 
            mc.exit()
               
    
     
     
        
 
