


from magiclick import MagiClick,ParaAddr
import adafruit_imageload
import terminalio,displayio,gc,time
from adafruit_display_text import label
from adafruit_display_shapes.rect import Rect
import random
import struct
import audiocore

import struct


mc = MagiClick()

mc.display.root_group=None
main_group = displayio.Group()

def getCount():

    return mc.read_para(ParaAddr.COUNTER_NEW)

def setCount(cnt):
    pass
    
    
print(getCount()) 

gc.collect()

IMG_WIDTH=96
IMG_HEIGHT=96
IMG_FRAME=3 #gif frames 

 

mc.display.root_group=None 
main_group = displayio.Group()


wavpath = 'audio/counter/muyu.wav'
 
def playwave():
    mc.audio_enable()
    
    try :
        wave_file = open(wavpath, "rb")
        wave = audiocore.WaveFile(wave_file)
        mc.audio.play(wave)
        while mc.audio.playing:
            pass
        wave.deinit()
        wave_file.close()
        wave_file=None
        gc.collect()
         
    except Exception as e : 
        print (e)
    
    mc.audio_disable()
    pass

# background = Rect(0,0, display.width-1,display.height-1,fill=0xffffff)
 


 

 

img_group = displayio.Group(scale=1)

sprit_sheet,palette = adafruit_imageload.load('/images/counter/gongde3.bmp',bitmap = displayio.Bitmap,palette = displayio.Palette)
 
palette.make_transparent(0)

spirite = displayio.TileGrid(sprit_sheet,pixel_shader=palette, 
                             width=1,
                             height=1,
                             tile_width=IMG_WIDTH,
                             tile_height=IMG_HEIGHT                             
                             )
palette.make_transparent(0)
spirite[0]=2
spirite.x = (mc.display.width-IMG_WIDTH*1)//2
 
img_group.append(spirite) 





# label
cntlabel = label.Label(terminalio.FONT,color = 0x00ff00,scale=2)
cntlabel.anchor_point = (0.5,0.0)
cntlabel.anchored_position = (mc.display.width / 2, 105)
cntlabel.text='{}'.format(getCount())

# main_group.append(background)
main_group.append(img_group)
main_group.append(cntlabel)
mc.display.root_group =main_group
mc.display.brightness = 1.0
 
print(gc.mem_free())
gc.collect()
print(gc.mem_free())


class Controls:
    def __init__(self):
        self.frame_cnt = 0
        self.start = False
        self.end = False
        self.cnt=0
        self.f_destroy=False
      



def main():
    controls = Controls()
    controls.cnt=getCount()
    key=-1
    while True:
        key_event = mc.keys.events.get()
        if key_event:
            if key_event.pressed:
                key = key_event.key_number
        else:
             key=-1
        if key==0:
            key=-1
            playwave()
            controls.cnt+=1
            cntlabel.text =str(controls.cnt)
            controls.start = True
            
            setCount(controls.cnt)
            print( controls.cnt)
            
            spirite[0] = controls.frame_cnt
            for i in range(IMG_FRAME):
                spirite[0] = i
                controls.frame_cnt+=1
                if controls.frame_cnt== IMG_FRAME:
                    controls.end = True
                    controls.frame_cnt=0
                    controls.start=False
                    break
                time.sleep(0.02)
                
        elif key==2  :
            controls.f_destroy=True
            mc.write_para(ParaAddr.COUNTER_NEW,controls.cnt)
            mc.exit()
        
        elif key==1  :             
            mc.write_para(ParaAddr.COUNTER_NEW,0)
            controls.cnt=0
            cntlabel.text =str(controls.cnt)
             
             
        else:
            time.sleep(0.1)
            
        acceleration = mc.imu.acceleration
        if acceleration[2] > 8.0:
            mc.write_para(ParaAddr.COUNTER_NEW,controls.cnt)
            mc.exit()
            
            
    
main() 
 
 













