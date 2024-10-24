from magiclick import MagiClick
import asyncio,time
import random 
import terminalio,displayio
from adafruit_display_text import label

mc = MagiClick()

class Dice:
    def __init__(self):
        self.value=0
        self.f_start=False
        self.f_loop = False
        self.f_stop = False
        self.f_destroy =False
        
    def roll(self):
        self.value = random.randint(0,9)
        
    
    def start(self):
        pass
    
    def stop(self):
        pass
        
        
mc.display.root_group=None 
main_group = displayio.Group()

# sprit_sheet,palette = adafruit_imageload.load('/images/gongde.bmp',bitmap = displayio.Bitmap,palette = displayio.Palette)
# palette.make_transparent(0)
# 
# spirite = displayio.TileGrid(sprit_sheet,pixel_shader=palette,
#                              width=1,
#                              height=1,
#                              tile_width=96,
#                              tile_height=96                             
#                              )
# spirite[0]=0
# spirite.x = (display.width-IMG_WIDTH)//2

from adafruit_bitmap_font import bitmap_font
from displayio import Bitmap

WRAP_WIDTH = 64



# fontFile = "fonts/ChillRoundM-12.pcf"
fontFile = "fonts/LibreBodoniv2002-Bold-27.bdf"

font = bitmap_font.load_font(fontFile, Bitmap)
# label
dice_label = label.Label(font,color = 0x00ff00,scale=3)
dice_label.anchor_point = (0.5,0.5)
dice_label.anchored_position = (mc.display.width / 2, mc.display.height/2)
dice_label.text='0'

# main_group.append(spirite)
main_group.append(dice_label)
mc.display.root_group =main_group    
        
palette=[0xff00ff,0xff0000,0x0000ff,0x00ff00,0x00ffff]

mc.display.brightness=1.0

TICK_DICE = 1.0

# 
async def draw(dice):
    starttick=0.0
    while True:
        if dice.f_start==True:
            starttick = time.monotonic()
            dice.f_start=False            
            dice.f_loop=True
        if dice.f_loop==True:
            dice.roll()
            dice_label.text= str(dice.value)
            dice_label.color = palette[random.randint(0,4)]
            if time.monotonic()-starttick >= TICK_DICE:
                dice.f_loop=False
                dice.f_stop=True
        
        if dice.f_stop==True:
            dice.f_stop = False
             
        await asyncio.sleep(0.1)
        if dice.f_destroy:
            break
        
    
#     
async def imu_handle(dice):
    while True:
        acceleration = mc.imu.acceleration
        if abs(acceleration[0]) > 20.0 or abs(acceleration[1]) > 20.0 or abs(acceleration[2]) > 20.0:
            dice.f_start=True
            
            
#         if dice.f_start:
#             if abs(acceleration[0]) < 1.0 and abs(acceleration[1]) < 1.0 and abs(acceleration[2]) < 10.0:
#                 dice.f_start=False            
        
        await asyncio.sleep(0.1)
        
        if dice.f_destroy:
            break
        
         
        if acceleration[2] > 8.0:            
            mc.exit()
            break


async def button_handle(dice):
    while True:
        await asyncio.sleep(0.2)
        key_event = mc.keys.events.get()
        if key_event:
            if key_event.released:
                key = key_event.key_number
        else:
             key=-1
        
        if key==0:            
            dice.f_start=True
        
        if key==2:
            dice.f_destroy=True
            mc.exit()
            break
        
        


# 
async def main():
    mc.display.brightness=1.0 
    dice =Dice()
    draw_task = asyncio.create_task(draw(dice))
    imu_task = asyncio.create_task(imu_handle(dice))
    btn_task = asyncio.create_task(button_handle(dice))
    await asyncio.gather(draw_task, imu_task,btn_task)


#




asyncio.run(main())       
    
 
    


