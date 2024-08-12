'''
pomodoro.py
v0.2.0
    20230725
    modify playwave
    
v0.1.0
    20230723
    first release
    
'''




from magiclick import MagiClick
from adafruit_display_text import label
import array
import math
import time,displayio,terminalio,gc
import audiocore
from audiomp3 import MP3Decoder 
from adafruit_progressbar.horizontalprogressbar import (
    HorizontalProgressBar,
    HorizontalFillDirection,
)

mc = MagiClick()
WORK = 25
SHORTBREAK = 5
COLOR_STOPED = 0xff0000
COLOR_STARTED = 0x00ff00



# You have to specify some mp3 file when creating the decoder
mp3 = open('audio/pomodoro/break.mp3', "rb")
decoder = MP3Decoder(mp3)
audio = mc.audio
 

def playwave(filename):
    mc.audio_enable()
    try :
        decoder.file = open('audio/pomodoro/{}'.format(filename), "rb")
        audio.play(decoder)
        print("playing", filename)

        # This allows you to do other things while the audio plays!
        while audio.playing:
            pass
         
    except Exception as e : 
        print (e)
     
    mc.audio_disable()
    pass



# Define the Pomodoro class
class Pomodoro:
    def __init__(self,worktime:int,shortbreaktime:int):
        self.workmode=0
        self.shortbreakmode=1
        
        self.worktime = worktime
        self.shortbreaktime = shortbreaktime
        
        self.time=self.worktime
        self.mode= self.workmode
        self.minutes = self.worktime
        self.seconds = 0
        self.is_running = False

    def display_time(self):
        # Calculate the remaining time in minutes and seconds
        remaining_minutes = self.minutes
        remaining_seconds = self.seconds

        # Display the remaining time
        print(f"Time remaining: {remaining_minutes:02d}:{remaining_seconds:02d}")
    def setmode(self,mode):
        if mode==self.workmode:            
            self.time = self.worktime
        elif mode==self.shortbreakmode:
            self.time = self.shortbreaktime
        self.mode = mode
        
        
    def getmode(self):
        return self.mode
        
        
    def reset(self):
        # Reset the timer to the default values
        self.minutes = self.time 
        self.seconds = 0
        self.is_running = False

    def start(self):
        # Start the timer
        self.is_running = True

    def pause(self):
        # Pause the timer
        self.is_running = False

    def toggle(self):
        # Toggle the timer between running and paused
        self.is_running = not self.is_running
        

# Create an instance of the Pomodoro class
pomodoro = Pomodoro(WORK,SHORTBREAK)


mc.display.root_group=None
main_group = displayio.Group()

# label
t_label = label.Label(terminalio.FONT, color=COLOR_STARTED, scale=4)
t_label.anchor_point = (0.5, 0.0)
t_label.anchored_position = (mc.display.width / 2, 40)
t_label.text = f"{WORK:02d}:{00:02d}"

mode_label = label.Label(terminalio.FONT, color=0xB4D7FA, scale=2)
mode_label.anchor_point = (0.5, 0.0)
mode_label.anchored_position = (mc.display.width / 2, 10)
mode_label.text = "Pomodoro" 

main_group.append(t_label)
main_group.append(mode_label) 


# set progress bar width and height relative to board's display
width = mc.display.width - 10
height = 15

x = mc.display.width // 2 - width // 2
y = mc.display.height // 2+30

# Create a new progress_bar object at (x, y)
progress_bar = HorizontalProgressBar(
    (x, y), (width, height), direction=HorizontalFillDirection.LEFT_TO_RIGHT
)

# Append progress_bar to the splash group
main_group.append(progress_bar)
mc.display.root_group =main_group

mc.display.brightness=1.0
# playwave('go.wav')

t_old=0
# Main loop to update and display the timer
while True:
    if (time.monotonic()-t_old) >= 1.0:
        t_old = time.monotonic()
        if pomodoro.is_running:
        # Decrease the timer by 1 second
            if pomodoro.seconds > 0:
                pomodoro.seconds -= 1
            elif pomodoro.minutes > 0:
                pomodoro.minutes -= 1
                pomodoro.seconds = 59
            else:
                mode = pomodoro.getmode()
                if mode==pomodoro.workmode:
                    pomodoro.setmode(pomodoro.shortbreakmode)
                    mode_label.text = "Break" 
                    t_label.color = COLOR_STOPED
                elif mode==pomodoro.shortbreakmode:
                    pomodoro.setmode(pomodoro.workmode)
                    mode_label.text = "Pomodoro" 
                    t_label.color = COLOR_STOPED
                # Timer has reached 0, reset the timer
                pomodoro.reset()
                mode = pomodoro.getmode()
                if mode == pomodoro.workmode:
                    playwave('go.mp3')
                elif mode==pomodoro.shortbreakmode:
                    playwave('break.mp3')
            # Display the timer
            pomodoro.display_time()
            t_label.text = f"{pomodoro.minutes:02d}:{pomodoro.seconds:02d}"
            progress_bar.value = int((1- ((pomodoro.minutes*60+pomodoro.seconds)/(pomodoro.time*60) ))*(progress_bar.maximum - progress_bar.minimum))
    

    
    key_event = mc.keys.events.get()
    if key_event:
        if key_event.released:
            key = key_event.key_number
    else:
         key=-1
         
    if key==0:
        if not pomodoro.is_running:
            t_label.color = COLOR_STARTED
            pomodoro.start()
            t_old = time.monotonic()
        else:
            t_label.color = COLOR_STOPED
            pomodoro.pause()
    if key==2  :
         
        mode = pomodoro.getmode()
        if mode==pomodoro.workmode:
            pomodoro.setmode(pomodoro.shortbreakmode)
            mode_label.text = "Break" 
        elif mode==pomodoro.shortbreakmode:
            pomodoro.setmode(pomodoro.workmode)
            mode_label.text = "Pomodoro" 
        pomodoro.reset()
        t_label.color = COLOR_STARTED
        t_label.text = f"{pomodoro.minutes:02d}:{pomodoro.seconds:02d}"
        progress_bar.value = progress_bar.minimum
            
                
            
    # Wait for 1 second
    time.sleep(0.05)
    
    acceleration = mc.imu.acceleration
    if acceleration[2] > 8.0:        
        mc.exit()
    
    




