import gifio,displayio,time,terminalio
from magiclick import MagiClick,ParaAddr
from adafruit_display_text import label
from adafruit_display_shapes.rect import Rect
from audiomp3 import MP3Decoder

def getCount():

    return mc.read_para(ParaAddr.COUNTER_NEW)

def setCount(cnt):
    pass

mc = MagiClick()
mc.display.brightness = 1.0

background = Rect(0,0, mc.display.width,mc.display.height,fill=0x000000)


bg =displayio.Group(scale =1)
bg.append(background)

try:
    odg = gifio.OnDiskGif("/images/counter/earth-ezgif.com-resize.gif")
    face = displayio.TileGrid(
        odg.bitmap,
        pixel_shader=displayio.ColorConverter(
            input_colorspace=displayio.Colorspace.RGB565_SWAPPED
        ),
        
    )
    bg.append(face)
except:
    pass
print(odg.width)
face.x= (mc.display.width-odg.width*1)//1//2
face.y= (96-odg.height*1)//1//2
odg.next_frame()

main_group = displayio.Group()
main_group.append(bg)
 

# label
cntlabel = label.Label(terminalio.FONT,color = 0x00ff00,scale=2)
cntlabel.anchor_point = (0.5,0.0)
cntlabel.anchored_position = (mc.display.width / 2, 105)
cntlabel.text='{}'.format(getCount())

main_group.append(cntlabel)

mc.display.root_group= main_group

class Controls:
    def __init__(self):
        self.frame_cnt = 0
        self.start = False
        self.end = False
        self.cnt=0
        self.f_destroy=False
        
        
controls = Controls()
controls.cnt=getCount()
key=-1


# You have to specify some mp3 file when creating the decoder
mp3 = open('audio/counter/wooden-door-slamming-open-79933.mp3', "rb")
decoder = MP3Decoder(mp3)
audio = mc.audio
def playwave():
    mc.audio_enable()
    try :
#         decoder.file = open('audio/counter/{}'.format(filename), "rb")
        audio.play(decoder)
#         print("playing", filename)

        # This allows you to do other things while the audio plays!
        while audio.playing:
            pass
         
    except Exception as e : 
        print (e)
     
    mc.audio_disable()
    pass

while True:
#     pass
#     next_delay = odg.next_frame()
#     time.sleep(next_delay)
    


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
        
#         spirite[0] = controls.frame_cnt
#         for i in range(IMG_FRAME):
#             spirite[0] = i
#             controls.frame_cnt+=1
#             if controls.frame_cnt== IMG_FRAME:
#                 controls.end = True
#                 controls.frame_cnt=0
#                 controls.start=False
#                 break
#             time.sleep(0.02)
        for i in range(3):    
            next_delay = odg.next_frame()
            time.sleep(next_delay)
        controls.start=False
        controls.end = True
            
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

