'''
v0.2.0
    20230725
    add get_weather()
        gc.collect()

v0.1.0
    20230723
    first release
    
'''

from magiclick import MagiClick

import os
import ssl
import time

import board
import displayio
import terminalio,supervisor
import socketpool
import adafruit_requests
import adafruit_imageload
from adafruit_display_text import bitmap_label

mc = MagiClick()

# Define time interval between requests
time_interval = 600  # set the time interval to 10 minutes

# Use cityname, country code where countrycode is ISO3166 format.
# E.g. "New York, US" or "London, GB"
LOCATION = os.getenv('LOCATION')

# Set up where we'll be fetching data from
DATA_SOURCE = "http://api.openweathermap.org/data/2.5/weather?q="+LOCATION
DATA_SOURCE += "&appid="+os.getenv('openweather_token') +"&units=metric"
# You'll need to get a token from openweather.org, looks like 'b6907d289e10d714a6e88b30761fae22'
DATA_LOCATION = []
 




from adafruit_bitmap_font import bitmap_font
font_file = "fonts/LeagueSpartan-Bold-16.bdf"
font = bitmap_font.load_font(font_file)


# Set up display a default image 
#image, 8bit png
image, palette = adafruit_imageload.load("/images/weather/icons8-sync-96.png")
# Set the transparency index color to be hidden
palette.make_transparent(0)

tile_grid = displayio.TileGrid(image,pixel_shader = palette)
tile_grid.x = mc.display.width // 2 - tile_grid.tile_width // 2
tile_grid.y = mc.display.height // 2 - tile_grid.tile_height // 2

group = displayio.Group()
group.append(tile_grid)

# Create label for displaying temperature data
loc_area = bitmap_label.Label(font, scale=1)
loc_area.anchor_point = (0.0, 0)
loc_area.anchored_position = (0, 0)

wewather_area = bitmap_label.Label(terminalio.FONT, scale=1)
wewather_area.anchor_point = (0, 1.0)
wewather_area.anchored_position = (0, mc.display.height)
wewather_area.txet = "1234"


temp_area = bitmap_label.Label(font, scale=1)
temp_area.anchor_point = (1.0, 1.0)
temp_area.anchored_position = (mc.display.width, mc.display.height)
temp_area.txet = ""
# Create main group to hold all display groups
main_group = displayio.Group()
main_group.append(group)
main_group.append(loc_area)
main_group.append(temp_area)
main_group.append(wewather_area)
# Show the main group on the display
mc.display.root_group= main_group

# Define function to get the appropriate weather icon
def get_weather_condition_icon(weather_condition):
    if "cloud" in weather_condition.lower():
        return "/images/weather/icons8-cloudy-64_.png"
    elif "rain" in weather_condition.lower():
        return "/images/weather/icons8-rain-64_.png"
    elif "snow" in weather_condition.lower():
        return "/images/weather/icons8-snowy-64_.png"
    elif "clear" in weather_condition.lower():
        return "/images/weather/icons8-sunny-64_.png"
    else:
        return "/images/weather/icons8-sync-96.png"

# Define function to update the background image based on weather conditions
def set_background(weather_condition, background_tile_grid):
    bitmap_path = get_weather_condition_icon(weather_condition)    
    image, palette = adafruit_imageload.load(bitmap_path)
    palette.make_transparent(0)
    background_tile_grid.bitmap = image
    background_tile_grid.pixel_shader = palette

def get_weather():
    import wifi
    # Create a socket pool and session object for making HTTP requests
    pool = socketpool.SocketPool(wifi.radio)
    if temp_area.txet == "":
        set_background('sync',tile_grid)
    mc.display.refresh()
    wifi.radio.enabled = True
    wifi.radio.start_station()
    # Get wifi AP credentials from a settings.toml file
    wifi_ssid = os.getenv("WIFI_SSID")
    wifi_password = os.getenv("WIFI_PASSWORD")
    if wifi_ssid is None:
        print("WiFi credentials are kept in settings.toml, please add them there!")
        return
#         raise ValueError("SSID not found in environment variables")
     
    try:
        wifi.radio.connect(wifi_ssid, wifi_password)
    except ConnectionError:
        print("Failed to connect to WiFi with provided credentials")
        return
    
    requests = adafruit_requests.Session(pool, ssl.create_default_context())
    print("Getting weather for {}".format(LOCATION))
    
    # Fetch weather data from OpenWeatherMap API
    print("Fetching json from", DATA_SOURCE)
    response = requests.get(DATA_SOURCE)
    print(response.json())

    # Extract temperature and weather condition data from API response
    
    current_weather_condition = response.json()["weather"][0]["main"]
    current_temp = response.json()["main"]["temp"]

    print("Weather condition: ", current_weather_condition)


    # Update label for displaying temperature data
    loc_area.text = LOCATION
    temp_area.text = f"{current_temp:.1f}°C"
    wewather_area.text = current_weather_condition

    # Update background image
    set_background(current_weather_condition, tile_grid)
    
    wifi.radio.stop_station()
    wifi.radio.enabled = False
    
    
mc.display.brightness=1.0 

get_weather()
now = time.monotonic()
old = now

while True:
    now =  time.monotonic()
    if (now-old) >= time_interval:
        old = time.monotonic()
        get_weather()
        gc.collect()
        
    time.sleep(0.2)
    
    key_event = mc.keys.events.get()
    if key_event:
        if key_event.pressed:
            key = key_event.key_number
    else:
         key=-1
         
         

    if key==0:
        key=-1
        get_weather()

         
    elif key==2 or key==1:
        print('exit')
        mc.exit() 
     
                
    acceleration = mc.imu.acceleration
    if acceleration[2] > 8.0:
        mc.exit()






