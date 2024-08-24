'''
v0.2.3
    20230913
    del fail info ...
    fix 2dian
v0.2.2
    20230824
    use ntp
v0.2.1
    20230802
    delay time:10s

v0.2.0
    20230723
    Fix unexpected breaks, i2s
    add week
    delete gif
'''




from magiclick import MagiClick

import socketpool
import os,displayio,supervisor,gc,terminalio
import rtc
import time
import audiocore
import board
import audiobusio
from adafruit_display_text import label
import adafruit_ntp

mc = MagiClick()

spHour = ["12", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"]
spMinDec = ["0", "10", "20", "30", "40", "50"]
spMinSpecial = ["11", "12", "13", "14", "15", "16", "17", "18", "19"]
spMinLow = ["1", "2-", "3", "4", "5", "6", "7", "8", "9"]


def playwave(filename):
 
    mc.audio_enable()
     
    try :
        wave_file = open('audio/cn_girl/{}'.format(filename), "rb")
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


def sayTimeCN(hour,  minutes):
    pm=False
    if hour>=12:
        pm=True     

#     playwave("audio/cn_girl/the time is.wav")
#     if pm:
#         playwave("afternoon.wav")
#     else:
#         playwave("morning.wav")

    hour = hour % 12

    playwave("{}.wav".format(spHour[hour]))
    playwave("点.wav")
    
    if minutes == 0:
        pass
#         playwave("zheng.wav") 
    elif minutes <= 10 or minutes >= 20:
        playwave("{}.wav".format(spMinDec[minutes // 10]))
        if minutes % 10:
            playwave("{}.wav".format(spMinLow[(minutes % 10) - 1]))             

        playwave("分.wav")

    else:
        playwave("{}.wav".format(spMinSpecial[minutes - 11])) 
        playwave("分.wav")
        
        
 


 
time_now = time.localtime()
print(time_now) 

mc.display.root_group=None
main_group = displayio.Group()

from adafruit_bitmap_font import bitmap_font
font_file = "fonts/LeagueSpartan-Bold-16.bdf"
font = bitmap_font.load_font(font_file)
# font = terminalio.FONT

# label
hour_label = label.Label(terminalio.FONT, color=0x00ff00, scale=6)
hour_label.anchor_point = (1.0, 0.0)
hour_label.anchored_position = (mc.display.width-1, 0)
hour_label.text = "{:0>2d}".format(time_now.tm_hour)

minute_label = label.Label(terminalio.FONT, color=0x00ffff, scale=6)
minute_label.anchor_point = (1.0, 0.0)
minute_label.anchored_position = (mc.display.width-1, 64)
minute_label.text = "{:0>2d}".format(time_now.tm_min)

# gc_label = label.Label(terminalio.FONT, color=0xff00ff, scale=1)
# gc_label.anchor_point = (0.5, 0.0)
# gc_label.anchored_position = (display.width / 2+40, 110)
# gc_label.text = "{}KB".format(gc.mem_free()/1024)

info_label = label.Label(terminalio.FONT, color=0x00ff00, scale=2)
info_label.anchor_point = (0.5, 0.5)
info_label.anchored_position = (64, 64)
info_label.text = "Time \nSyncing..."
info_label.hidden = True
info_label.background_color  = 0xff00ff


WEEK_COLOR_NOW = 0xCCCCCC
WEEK_COLOR_NOTNOW=0x444444
week_id = time_now.tm_wday
week_label=[]
weeks = ("MON","TUE","WED","THU","FRI","SAT","SUN")
for i in range(7):
    wlabel = label.Label(font, color=WEEK_COLOR_NOTNOW, scale=1)
    wlabel.anchor_point = (0.0, 0.0)
    wlabel.anchored_position = (0, i*19)
    wlabel.text = f"{weeks[i]}"
    week_label.append(wlabel)
    main_group.append(wlabel)
    
week_label[week_id].color = WEEK_COLOR_NOW

# print(time_now.tm_wday)
# print(week_id)

main_group.append(hour_label)
main_group.append(minute_label)
# main_group.append(gc_label)
main_group.append(info_label)
mc.display.root_group = main_group
mc.display.refresh()
mc.display.brightness=1.0
# syncTime()

time_now = time.localtime() 
sayTimeCN(time_now.tm_hour, time_now.tm_min) 
 

now = time.monotonic()
old = now
 
key=-1
acceleration = mc.imu.acceleration
f_time_sayed=False



def syncTime():
    import wifi
    print(wifi.radio.enabled)
    wifi.radio.enabled = True
    wifi.radio.start_station()
    info_label.hidden = False
    # Get wifi AP credentials from a settings.toml file
    wifi_ssid = os.getenv("WIFI_SSID")
    wifi_password = os.getenv("WIFI_PASSWORD")
    if wifi_ssid is None:
        print("WiFi credentials are kept in settings.toml, please add them there!")
        raise ValueError("SSID not found in environment variables")
    info_label.text = 'Time \nSyncing..'
    mc.display.refresh()
    try:
        wifi.radio.tx_power = 8.5
        wifi.radio.connect(wifi_ssid, wifi_password)
        print("my IP addr:", wifi.radio.ipv4_address)
    except ConnectionError:
        print("Failed to connect to WiFi with provided credentials")
        info_label.hidden = True
        return
         

    pool = socketpool.SocketPool(wifi.radio)
    ntp = adafruit_ntp.NTP(pool, tz_offset=os.getenv("TIMEZONE"), cache_seconds=3600)

    # NOTE: This changes the system time so make sure you aren't assuming that time
    # doesn't jump.
    
    for i in range(3):
        try:
            rtc.RTC().datetime = ntp.datetime
            info_label.text = 'OK'
            mc.display.refresh()
            break
        except:
            info_label.text = 'retry'
            mc.display.refresh()
            pass
    time.sleep(0.5)
    t =time.localtime()
    hour_label.text = f'{t.tm_hour:02d}'
    minute_label.text = f'{t.tm_min:02d}'
    week_label[week_id].color = WEEK_COLOR_NOTNOW
    week_label[time_now.tm_wday].color = WEEK_COLOR_NOW
    weekid = time_now.tm_wday
    info_label.hidden = True
    wifi.radio.stop_station()
    wifi.radio.enabled = False
    gc.collect()
    print(gc.mem_free())
    return 



while True:
    now =  time.monotonic()
    if (now-old) >= 10.0:
        old = time.monotonic()
        time_now = time.localtime()
#         print(time_now)
        gc.collect()
        hour_label.text = "{:0>2d}".format(time_now.tm_hour)
        minute_label.text = "{:0>2d}".format( time_now.tm_min)
#         gc_label.text = "{}KB".format(gc.mem_free()/1024)
        
        if time_now.tm_wday != week_id:
#             print(time_now.tm_wday)
#             print(week_id)
            week_label[week_id].color = WEEK_COLOR_NOTNOW
            week_label[time_now.tm_wday].color = WEEK_COLOR_NOW
            weekid = time_now.tm_wday
            
        
        if time_now.tm_min==0:            
            if time_now.tm_hour>7 and time_now.tm_hour<24:
                if f_time_sayed ==False:
                    f_time_sayed=True
                    sayTimeCN(time_now.tm_hour, time_now.tm_min)
        else:
            if f_time_sayed:
                f_time_sayed = False
            
        
    # print(random.randint(0,99))    
        
    # Sleep for the frame delay specified by the GIF,
# minus the overhead measured to advance between frames.
#     time.sleep(max(0, next_delay - overhead))
#     odg.next_frame()
    
    time.sleep(0.2)
#     print(gc.mem_free())
    key_event = mc.keys.events.get()
    if key_event:
        if key_event.pressed:
            key = key_event.key_number
    else:
         key=-1
         
    if key==0:
        key=-1
        sayTimeCN(time_now.tm_hour, time_now.tm_min)
 
    elif key==2:
        print('exit')
        mc.exit()
    
    elif key==1:
        key=-1
        syncTime()
     
                
    acceleration = mc.imu.acceleration
    if acceleration[2] > 8.0:
        mc.exit()
                
             
 
         











