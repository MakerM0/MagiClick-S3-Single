'''
MakerM0
v0.2.0
    20240612
    ported to cpy 9.x
v0.1.0
    20240425
    first release
'''

from magiclick import MagiClick,ParaAddr
import time
from random import randint
from micropython import const
import board
import terminalio
import displayio
import adafruit_imageload
from adafruit_display_shapes.circle import Circle
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.line import Line
import digitalio
import simpleio
from adafruit_display_text import label
import random 
from magiclick import *
import gc

mc = MagiClick()

birdFile = "/images/game/frame.bmp"
pipedownFile = "/images/game/pipe_down.bmp"
pipeupFile = "/images/game/pipe_up.bmp"

K1_PRESSED=0
K1_RELEASED=10
k1_state = False


pipe_distance = 40

now = time.monotonic()
old= now
old_bird= now
old_pipe= now

frame_id=0

new_game = False
game_over=False 

total_score = 0





group = displayio.Group(scale=1)


'''backgound '''

background = displayio.Bitmap(128,128,1)
background_pal = displayio.Palette(1)
background_pal[0] = 0x87CEFA

bg_grid = displayio.TileGrid(background,pixel_shader=background_pal,x=0,y=0)

 

group.append(bg_grid)

#  bird sprite setup
bird, bird_pal = adafruit_imageload.load(birdFile,
                                             bitmap=displayio.Bitmap,
                                             palette=displayio.Palette)

#  creates a transparent background for bird
bird_pal.make_transparent(0)
bird_grid = displayio.TileGrid(bird, pixel_shader=bird_pal,
                                 width=1, height=1,
                                 tile_height=32, tile_width=32,
                                 default_tile=0)
bird_grid.x = 0
bird_grid.y = 0 

bird_group = displayio.Group()
bird_group.append(bird_grid)



'''  pipe sprite setup'''
pipe_down, pipe_down_pal = adafruit_imageload.load(pipedownFile,
                                             bitmap=displayio.Bitmap,
                                             palette=displayio.Palette)

#  creates a transparent background for pipe
# pipe_down_pal.make_transparent(0)
pipe_down_grid = displayio.TileGrid(pipe_down, pixel_shader=pipe_down_pal,
                                 width=1, height=1,
                                 tile_height=80, tile_width=13,
                                 default_tile=0)
pipe_down_grid.x = 120
pipe_down_grid.y = random.randrange(-60,0,5)


pipe_up, pipe_up_pal = adafruit_imageload.load(pipeupFile,
                                             bitmap=displayio.Bitmap,
                                             palette=displayio.Palette)

#  creates a transparent background for pipe
# pipe_up_pal.make_transparent(0)
pipe_up_grid = displayio.TileGrid(pipe_up, pixel_shader=pipe_up_pal,
                                 width=1, height=1,
                                 tile_height=80, tile_width=13,
                                 default_tile=0)
pipe_up_grid.x = 120
pipe_up_grid.y = pipe_down_grid.y+pipe_distance+80 

  
print(gc.mem_free())




#  text area for the running score
score_text = "0"
font = terminalio.FONT
score_color = 0x696969

#  text for "game over" graphic
game_over_text = label.Label(font, text = "         ", color = 0xFF00FF,scale =2)
# score text
score_area = label.Label(font, text=score_text, color=score_color,scale =2)
#  text for "new game" graphic
new_game_text = label.Label(font, text = "START", color = 0xF0f0FF,scale =2)

high_score_text = label.Label(font, text = "         ", color = 0x0000ff,scale =1)
# coordinants for text areas
# score_area.x = 0
# score_area.y = 24
score_area.anchor_point = (1.0, 0.0)
score_area.anchored_position = (mc.display.width-1, 0)

game_over_text.anchor_point = (0.5, 0.5)
game_over_text.anchored_position = (mc.display.width//2, mc.display.height//2-10)

high_score_text.anchor_point = (0.5, 0.5)
high_score_text.anchored_position = (mc.display.width//2, mc.display.height//2+10)

new_game_text.anchor_point = (0.5, 0.5)
new_game_text.anchored_position = (mc.display.width//2, mc.display.height//2)

 
# creating a text display group
text_group = displayio.Group()
text_group.append(score_area)
text_group.append(game_over_text)
text_group.append(high_score_text)
text_group.append(new_game_text)





'''
cloud
'''
posx = 0
posy = 0
circle_radius =20
cloud_color = 0xffffff
# Define Circle characteristics
 
circle1 = Circle(posx, posy, 4, fill=cloud_color )
circle2 = Circle(posx+5, posy+2, 5, fill=cloud_color)
circle3 = Circle(posx+12, posy, 4, fill=cloud_color)
circle4 = Circle(posx+9, posy-2, 3, fill=cloud_color)

cloud_group = displayio.Group()
cloud_group.append(circle1)
cloud_group.append(circle2)
cloud_group.append(circle3)
cloud_group.append(circle4)

cloud_group.y=20 

circle1 = Circle(posx, posy, 4, fill=cloud_color )
circle2 = Circle(posx+5, posy+2, 5, fill=cloud_color)
circle3 = Circle(posx+12, posy, 4, fill=cloud_color)
circle4 = Circle(posx+9, posy-2, 3, fill=cloud_color)

cloud_group1 = displayio.Group()
cloud_group1.append(circle1)
cloud_group1.append(circle2)
cloud_group1.append(circle3)
cloud_group1.append(circle4)

cloud_group1.y=40

'''ground '''
GREEN=0x7cfc00
DARKGREEN=0x006400
bg_group = displayio.Group()
for i in range(18):
    if i%2:
        color = GREEN
    else:
        color = DARKGREEN
    rect = Rect(0+i*8, 0, 8, 5, fill=color)
    bg_group.append(rect)
    
bg_group.y = 123

'''line'''
line1 = Line(0, 128-7, 128, 128-7, 0x000000)
line2 = Line(0, 128-6, 128, 128-6, 0x8B4513)


group.append(cloud_group1)
group.append(cloud_group)
group.append(bird_group)
 
group.append(pipe_down_grid)
group.append(pipe_up_grid)
group.append(text_group)

group.append(bg_group)
group.append(line1)
group.append(line2)

#  displaying main display group
mc.display.root_group = group
mc.display.brightness=1.0

gc.collect()
print(gc.mem_free()) 
while True:
    now = time.monotonic()
    
    key_event = mc.keys.events.get()
    if key_event:
        if key_event.pressed:
            key = key_event.key_number
            if key == 0:
                key= K1_PRESSED
        if key_event.released:
            key = key_event.key_number
            if key == 0:
                key = K1_RELEASED
    else:
         key=-1
         
    if key==K1_PRESSED:
        k1_state = True
    elif key== K1_RELEASED:
        k1_state = False
    
    if now>(old+0.05):
        old = time.monotonic()
        gc.collect()
        acceleration = mc.imu.acceleration
        if acceleration[2] > 8.0:
            mc.exit()
    
        
    mc.display.auto_refresh=False
    if now>(old_bird+0.02) and new_game==True:
        old_bird=now

        if k1_state==True:
            bird_grid.y -= 3
            
            if bird_grid.y <-16:
                game_over = True 
                
            bird_grid[0]= frame_id
            frame_id +=1
            if frame_id==3:
                frame_id=0
        else:
            bird_grid.y += 2
            if bird_grid.y > 128-24:
                bird_grid.y = 128-24
                game_over = True
    
    
    if now>(old_pipe+0.03) and new_game==True:
        cloud_group1.x-=3
        if cloud_group1.x<-10:
            cloud_group1.x=120
            cloud_group1.y= random.randrange(10,50,10)
        cloud_group.x -=2
        if cloud_group.x<-10:
            cloud_group.x=120
            cloud_group.y= random.randrange(40,90,10)
        
        
        old_pipe = now
        pipe_up_grid.x-=1
        pipe_down_grid.x-=1
        bg_group.x-=1
        if bg_group.x == -16:
            bg_group.x=0
        
    
        if pipe_down_grid.x<-13:
            pipe_down_grid.x=mc.display.width
            pipe_down_grid.y=random.randrange(-60,0,5)
            pipe_up_grid.x=mc.display.width
            pipe_up_grid.y=pipe_down_grid.y+pipe_distance+80
            
            total_score += 1
            score_area.text = str(total_score)
        
             

    
        if pipe_up_grid.x <= 10+20 and pipe_up_grid.x > 5 and (bird_grid.y>=pipe_up_grid.y-32+10 or bird_grid.y <= pipe_down_grid.y+80-10):
            game_over = True
            print(bird_grid.y,pipe_up_grid.x,pipe_down_grid.y,pipe_up_grid.y)  
         
 
    mc.display.refresh(target_frames_per_second=120)
    mc.display.auto_refresh=True
    
    if game_over==True:
        new_game_text.text='        '
        game_over_text.text = "GAME OVER"
        highScore = mc.read_para(ParaAddr.FLAPPY_HIGHSCORE)
        if highScore < total_score:
            highScore = total_score
            mc.write_para(ParaAddr.FLAPPY_HIGHSCORE,highScore)
        high_score_text.text = f'HighScore: {highScore}'
        score_area.text = str(total_score)
        game_over=False
        new_game=False
        time.sleep(1.0)
         
        
    if new_game == False:
        if k1_state==True:
            new_game = True
            new_game_text.text='            '
            game_over_text.text = "         "
            high_score_text.text = "         "
            score_area.text = "0"
            total_score=0            
            bird_grid.x = 0
            bird_grid.y = 0
            pipe_down_grid.x = 120
            pipe_down_grid.y = random.randrange(-60,0,5)
            pipe_up_grid.x = 120
            pipe_up_grid.y = pipe_down_grid.y+pipe_distance+80             
            print('new_game')
            time.sleep(0.5)            
            
        pass
    