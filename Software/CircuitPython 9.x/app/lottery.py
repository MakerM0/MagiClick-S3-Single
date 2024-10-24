from magiclick import MagiClick
import random ,time
import terminalio,displayio
from adafruit_display_text import label
from adafruit_display_shapes.circle import Circle
from adafruit_display_shapes.rect import Rect
from adafruit_bitmap_font import bitmap_font
from displayio import Bitmap
import gifio,os,gc
import  audiocore, audiomp3

mc = MagiClick()
mc.display.auto_refresh = False

# filetype:".bmp"
def get_files(base,filetype):
    files = list(filter(lambda x: x.endswith(filetype), os.listdir(base)))
    print(files)
    return files

def showimgs(widget,imglist):     
    displayio.Colorspace.RGB565
    try:
        widget.pop()
    except:
        pass
    
    bitmap = displayio.OnDiskBitmap(open("images/lottery/"+imglist[random.randint(0,len(imglist)-1)], "rb"))
    image = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader)
    widget.append(image)
 

def playmp3(mp3list):
 
    mc.audio_enable()
     
    try :
        wave_file = open('audio/lottery/{}'.format(mp3list[random.randint(0,len(mp3list)-1)]), "rb")
        wave = audiomp3.MP3Decoder(wave_file)
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

mp3list = get_files("audio/lottery/",".mp3")
print(len(mp3list))
imglist = get_files("images/lottery/",".bmp")
print(len(imglist))

try:
    odg = gifio.OnDiskGif("/images/lottery/icons8-stack-of-coins.gif")
    face = displayio.TileGrid(
        odg.bitmap,
        pixel_shader=displayio.ColorConverter(
            input_colorspace=displayio.Colorspace.RGB565_SWAPPED
        ),
        
    )
     
except:
    pass

print(odg.width)
face.x= 128-odg.width+5
face.y= 128-odg.height+5
odg.next_frame()
 
fontFile = "fonts/LeagueSpartan-Bold-16.bdf"

font = bitmap_font.load_font(fontFile, Bitmap)

fontFile = "fonts/LibreBodoniv2002-Bold-27.bdf"
font2 = bitmap_font.load_font(fontFile, Bitmap)


def generate_double_color_ball():
    # Generate 6 unique red balls (range 1-33)
    red_balls = []
    blue_balls = []
    for i in range(6):        
        while True:
            ball = random.randint(1, 34)
            if ball not in red_balls:
                break
        red_balls.append(ball)
    red_balls.sort()  # Sort the red balls in ascending order
    
    # Generate 1 blue ball (range 1-16)
    blue_ball = random.randint(1, 16)
    
    # Combine red balls and blue ball
    result = red_balls + [blue_ball]
    
    return result 


main_group = displayio.Group()
# background = Rect(0,0, mc.display.width,mc.display.height,fill=0xffffff)
# main_group.append(background) 
main_group.append(face) 

label_win = label.Label(font2,color = 0xffff00,scale=1)
label_win.anchor_point = (1.0,1.0)
label_win.anchored_position = (128-10, 128-10)

label_win.text='WIN' 
# main_group.append(label_win)
 
 
for j in range(2):
    for i in range(3):
        circle = Circle(16+45*i, 16+45*j, 16, fill=0xFF0000, outline=0xFF0000)
        main_group.append(circle)
        
circle = Circle(16, 16+45*2, 16, fill=0x0000FF, outline=0x0000FF)
main_group.append(circle)

# label
label_balls=[]

for i in range(7):
    label1 = label.Label(font,color = 0xffffff,scale=1)
    label1.anchor_point = (0.5,0.5)
    label1.anchored_position = (45*(i%3)+16, 45*(i//3)+16)
 
    label1.text='?'
    label_balls.append(label1)
    main_group.append(label1) 


 
image_group = displayio.Group()
 

main_group.append(image_group) # shows the image

image_group.hidden = True
mc.display.root_group =main_group
mc.display.brightness=1.0 
mc.display.refresh()


while True:
    time.sleep(0.1)
    key_event = mc.keys.events.get()
    if key_event:
        if key_event.pressed:
            key = key_event.key_number
    else:
         key=-1
    
    if key==0:
        key=-1
        result = generate_double_color_ball()
        for i in range(7):
            label_balls[i].text = f'{result[i]:02d}'
        showimgs(image_group,imglist)
        image_group.hidden = False
        mc.display.refresh()
        playmp3(mp3list)
#         time.sleep(1)
        image_group.hidden = True
        mc.display.refresh()
        

    
    
    acceleration = mc.imu.acceleration
    if acceleration[2] > 8.0:
        mc.exit()
    
    label_win.x = random.randint(60,62)
    label_win.y = random.randint(102,104)
    odg.next_frame()
    mc.display.refresh()
     
     





