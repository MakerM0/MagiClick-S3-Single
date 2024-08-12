from magiclick import MagiClick
import board
from adafruit_slideshow import PlayBackOrder, SlideShow,VerticalAlignment,HorizontalAlignment,


mc = MagiClick()
mc.display.brightness=1.0

slideshow = SlideShow(
    mc.display,
    None,
    folder="/images/photo/",
    loop=True,
    order=PlayBackOrder.ALPHABETICAL,
    dwell=4,
)

slideshow.h_align = HorizontalAlignment.CENTER
slideshow.v_align = VerticalAlignment.CENTER

while slideshow.update():
    acceleration = mc.imu.acceleration
    if acceleration[2] > 8.0:
        mc.exit()
    pass