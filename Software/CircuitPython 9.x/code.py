'''
v0.2.3
    20240929
    add png trans
    add background
v0.2.2
    202311
    fix func quit order
v0.2.1
    20230925
    modify app directory
v0.2.0
    20230723
    
    The icons is from here  https://icons8.com/

'''

import alarm
import supervisor
import os
from adafruit_display_shapes.rect import Rect
from adafruit_display_text import label
import adafruit_imageload
from adafruit_bitmap_font import bitmap_font
from displayio import Bitmap
import displayio,terminalio,time,gc
import microcontroller
print(gc.mem_free())
from magiclick import MagiClick
microcontroller.cpu.frequency=240000000
gc.collect()
mc = MagiClick()
mc.display.brightness=0.0


F_VBAT = False 
F_TEMPER = False 
 
print(gc.mem_free())
 
vbat=0
for i in range(10):    
    vbat += mc.get_batt()
    
vbat = int(vbat/10)

class Launch:
    def __init__(self):
        self.file_list = self.get_files('/app/')
        self.file_cnt = len(self.file_list)
        self.index=0
        pass    

    def get_files(self, base):
        files = os.listdir(base)
        file_names = []
        for isdir,filetext in enumerate(files):
            if  filetext.endswith('.py') :
                if filetext  not   in  ('code.py','launch.py','boot.py'):                
                    stats = os.stat(base+filetext)
                    isdir = stats[0]&0x4000
                    if isdir:
                        pass
    #                     file_names.append((filetext,True))
                    else:
                        file_names.append(filetext)
                        
        return file_names

    # draw func 
    def draw_img(self,label,filename):
#         gc.collect()
        label.text = filename.split('.')[0]
        try :            
            icongroup.pop()
        except:
            pass
        

        
        try:
            image, palette = adafruit_imageload.load('/app/icon/' + label.text + '.png')
            palette.make_transparent(0)
            tile_grid = displayio.TileGrid(image,pixel_shader = palette)
            tile_grid.x = (mc.display.width - tile_grid.tile_width) // 2
            tile_grid.y = (mc.display.height  - tile_grid.tile_height) // 2 -10
        except Exception as e:
            image, palette = adafruit_imageload.load('/app/icon/icons8-app.png')
            palette.make_transparent(0)
            tile_grid = displayio.TileGrid(image,pixel_shader = palette)
            tile_grid.x = (mc.display.width - tile_grid.tile_width) // 2
            tile_grid.y = (mc.display.height  - tile_grid.tile_height) // 2 -10
            pass
        icongroup.append(tile_grid)
#         label.color =  int(sum(palette)/(len(palette)-1))
        label.color =  0xaaaaaa
#         label.background_color =  0xaaaaaa
#         gc.collect()
        return image
 
launch = Launch()
# launch.file_list.sort()
# file_list = get_files('/')
# file_cnt = len(file_list)
print(launch.file_list)
print( launch.file_cnt)

launch.file_list.sort()
print(launch.file_list)
DISPLAY_WIDTH = mc.display.width
DISPLAY_HEIGHT = mc.display.height

launch.index =alarm.sleep_memory[0]
 

mc.display.root_group = None

# create base display group
displaygroup = displayio.Group()


try:
    fontFile = "fonts/ChillRoundM-12.pcf"
    font = bitmap_font.load_font(fontFile, Bitmap)
except:
    font = terminalio.FONT

# create display
# 纯色
# background = Rect(0,0,DISPLAY_WIDTH-1,DISPLAY_HEIGHT-1,fill = 0x000000)
# 壁纸
background = displayio.Group()
odb = displayio.OnDiskBitmap('/images/photo/容器 14.bmp')
face = displayio.TileGrid(odb, pixel_shader=odb.pixel_shader)
background.append(face)

# label
filelabel = label.Label(font,color = 0x67E1F6,scale=1)
filelabel.anchor_point = (0.5,0.0)
filelabel.anchored_position = (DISPLAY_WIDTH / 2, 100+5)
# filelabel.x = 10
# filelabel.y = 100
filelabel.text = launch.file_list[launch.index].split('.')[0]


# vbat label
vbatlabel = label.Label(terminalio.FONT,color = 0x777777,scale=1)
vbatlabel.anchor_point = (1.0,0.0)
vbatlabel.anchored_position = (DISPLAY_WIDTH-5, 0)
if(vbat>=4350):
    vbatlabel.text ='USB'
else:
    vbatlabel.text = f'{vbat} mV'

temperlabel = label.Label(terminalio.FONT,color = 0x777777,scale=1)
temperlabel.anchor_point = (0.0,0.0)
temperlabel.anchored_position = (0, 0)
temperlabel.text = f'{microcontroller.cpu.temperature}c'

icongroup = displayio.Group()


displaygroup.append(background)
displaygroup.append(icongroup)
displaygroup.append(filelabel)
if F_VBAT:
    displaygroup.append(vbatlabel)

if F_TEMPER:
    displaygroup.append(temperlabel)

mc.display.root_group = displaygroup

launch.draw_img(filelabel,launch.file_list[launch.index])


mc.display.brightness=1.0
import bitmaptools 

now = time.monotonic()
old= now

gc.collect()
print(gc.mem_free())
key=-1
mc.display.auto_refresh=False
mc.display.refresh()
microcontroller.cpu.frequency=160000000

    
while True:
    time.sleep(0.1)
    now = time.monotonic()
    if now>old+2 :
        old = now
        vbat = mc.get_batt()
        if(vbat>=4350):
            vbatlabel.text ='USB'
        else:
            vbatlabel.text = f'{vbat} mV'
        temperlabel.text = f'{microcontroller.cpu.temperature}c'
#         temperlabel.text = f'{gc.mem_free()}'
        mc.display.refresh()
         
    
    key_event = mc.keys.events.get()
    if key_event:
        if key_event.released:
            key = key_event.key_number
    else:
        key=-1
        
    if key==1:
        print('Left')
        launch.index -= 1
        if launch.index<0:
            launch.index = launch.file_cnt-1
        print(launch.index)
        launch.draw_img(filelabel,launch.file_list[launch.index])
        mc.display.refresh()
        gc.collect()
        print(gc.mem_free())
        
    elif key==2:
        print('Right')
        launch.index+=1
        if launch.index>=launch.file_cnt:
            launch.index = 0
        print(launch.index)
        launch.draw_img(filelabel,launch.file_list[launch.index])
        mc.display.refresh()
        gc.collect()
        print(gc.mem_free())
    elif key==0:
        microcontroller.cpu.frequency=240000000
        mc.display.refresh()
 
        print('OK')
        mc.display.brightness=0.0
        alarm.sleep_memory[0] = launch.index 
        startApp='/app/'+ launch.file_list[launch.index]
        supervisor.set_next_code_file(startApp)
        supervisor.reload()
#         gc.collect()
#         display.show(displaygroup)
        
        pass
    
    
    acceleration = mc.imu.acceleration
#     print(acceleration)
    if acceleration[0] <-3.0:
         
        print('Left')
        launch.index -= 1
        if launch.index<0:
            launch.index = launch.file_cnt-1
        print(launch.index)      
        
        image = launch.draw_img(filelabel,launch.file_list[launch.index])
        mc.display.refresh()
        gc.collect()
        print(gc.mem_free())
        
        time.sleep(0.5)
        
    elif acceleration[0] >3.0:
        print('Right')
        launch.index+=1
        if launch.index>=launch.file_cnt:
            launch.index = 0
        print(launch.index)       
        
        image = launch.draw_img(filelabel,launch.file_list[launch.index])
        mc.display.refresh()
        gc.collect()
        print(gc.mem_free())
        
        time.sleep(0.5)
 



