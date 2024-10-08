#!/usr/bin/env python

"""
A Python port of the Adafruit_PixelDust Arduino library.
Particle similation for "LED sand."
https://github.com/adafruit/Adafruit_Spectro_Pi
"""

# Gets code to pass both pylint & pylint3:
# pylint: disable=bad-option-value, useless-object-inheritance

from magiclick import MagiClick
import math,displayio
import random

mc=MagiClick()


# pylint: disable=too-few-public-methods
class Grain(object):
    """Per-grain object representing position and velocity. A list
       of these is generated by one's application or by calling the
       PixelDust.randomize() function."""

    def __init__(self, coord_x, coord_y):
        """Initialize grain position at specified coordinates
           and set velocity to 0."""
        self.position = [coord_x, coord_y]
        self.velocity = [0, 0]

class PixelDust(object):
    """Particle simulation class for "LED sand." This handles the
       "physics engine" part of a sand/rain simulation. It does not
       actually render anything itself and needs to work in conjunction
       with a display library to handle graphics. The term "physics" is
       used loosely here...it's a relatively crude algorithm that's
       appealing to the eye but takes many shortcuts with collision
       detection, etc."""

    def __init__(self, width, height, elasticity):
        self.width = width            # Dimensions of pixel grid
        self.height = height
        self.elasticity = -elasticity # Invert elasticity; multiply = bounce
        self.scale = 0.005
        self.num_grains = 0           # Grain list is not populated at start
        self.grains = None
        self.bitmap = None
        self.clear()                  # Allocates/inits self.bitmap

    def set_pixel(self, coord_x, coord_y):
        """Sets state of one pixel on the pixel grid. This can be used for
           drawing obstacles for sand to fall around. Call this function
           BEFORE placing any sand grains with the place() or randomize()
           functions. Setting a pixel does NOT place a sand grain there,
           only marks that location as an obstacle."""
        self.bitmap[int(coord_x)][int(coord_y)] = True

    def clear_pixel(self, coord_x, coord_y):
        """Clears state of one pixel on the pixel grid; the inverse of
           set_pixel(). Call this function BEFORE placing any sand grains
           with the place() or randomize() functions."""
        self.bitmap[int(coord_x)][int(coord_y)] = False

    def get_pixel(self, coord_x, coord_y):
        """Returns state of one pixel on the pixel grid; True if pixel is
           set (an obstacle), False if clear (grains can move here)."""
        return self.bitmap[int(coord_x)][int(coord_y)]

    def clear(self):
        """Clear the pixel grid contents (remove all obstacles)."""
        self.bitmap = [[False for _ in range(self.height)]
                       for _ in range(self.width)]

    def set_position(self, coord_x, coord_y):
        """Place one sand grain on the pixel grid. Returns True if grain is
           added, False if position is already occupied."""
        if self.bitmap[coord_x][coord_y]:
            return False # Position already occupied
        self.grains.append(Grain(coord_x, coord_y))
        self.bitmap[coord_x][coord_y] = True
        self.num_grains += 1
        return True

    def get_position(self, i):
        """Get Position of one sand grain on the pixel grid. Pass index
           of grain (0 to num_grains-1), returns X, Y coordinates."""
        return self.grains[i].position[0], self.grains[i].position[1]

    def randomize(self, num_grains):
        """Randomize grain coordinates. This assigns random starting
           locations to every grain in the simulation, making sure they do
           not overlap or occupy obstacle pixels placed with the set_pixel()
           function. The pixel grid should first be cleared with the clear()
           functions and any obstacles then placed with set_pixel(); don't
           randomize() on an already-active field."""
        max_grains = sum(x.count(False) for x in self.bitmap)
        num_grains = min(num_grains, max_grains)
        self.num_grains = 0
        self.grains = []
        # Populate grains array, avoiding occupied spaces
        for _ in range(num_grains):
            while not self.set_position(random.randrange(self.width),
                                        random.randrange(self.height)):
                pass

    # pylint: disable=too-many-nested-blocks, too-many-branches, too-many-statements
    def iterate(self, accel):
        """Run one iteration (frame) of the particle simulation.
           Pass in acceleration as a 3-tuple (X,Y,Z)."""

        # Scale from G to sub-pixel units, flip X axis
        accel = (accel[0] * -self.scale, accel[1] * self.scale,
                 accel[2] * self.scale)

        # A tiny bit of random motion is applied to each grain, so that tall
        # stacks of pixels tend to topple (else the whole stack slides across
        # the display). This is a function of the Z axis input, so it's more
        # pronounced the more the display is tilted (else the grains shift
        # around too much when the display is held level).

        noise = 0.025 - max(min(abs(accel[2]) / 4, 0.02), 0.005)

        # Apply 2D accel vector to grain velocities...
        for grain in self.grains:
            grain.velocity[0] += accel[0] + random.uniform(-noise, noise)
            grain.velocity[1] += accel[1] + random.uniform(-noise, noise)
            # Terminal velocity (in any direction) is 1.0 units -- 1 pixel --
            # which keeps moving grains from passing through each other and
            # other such mayhem. Though it takes some extra math, velocity is
            # clipped as a 2D vector (not separately-limited X & Y) so that
            # diagonal movement isn't faster than horizontal/vertical.
            velocity_squared = (grain.velocity[0] * grain.velocity[0] +
                                grain.velocity[1] * grain.velocity[1])
            if velocity_squared > 1.0:
                velocity = math.sqrt(velocity_squared)
                grain.velocity[0] /= velocity  # Maintain heading &
                grain.velocity[1] /= velocity  # limit magnitude

        # ...then update position of each grain, one at a time, checking for
        # collisions and having them react. This really seems like it
        # shouldn't work, as only one grain is considered at a time while
        # the rest are regarded as stationary. Yet this naive algorithm,
        # taking many not-technically-quite-correct steps, and repeated
        # quickly enough, visually integrates into something that somewhat
        # resembles physics. (I'd initially tried implementing this as a
        # bunch of concurrent and "realistic" elastic collisions among
        # circular grains, but the calculations and volume of code quickly
        # got out of hand for my tiny dinosaur brain.)

        for grain in self.grains:
            newx = grain.position[0] + grain.velocity[0] # New position
            newy = grain.position[1] + grain.velocity[1] # in grain space
            if newx < 0:                             # If going out of bounds,
                newx = 0                             # keep it inside,
                grain.velocity[0] *= self.elasticity # and bounce off wall
            elif newx >= self.width:
                newx = self.width - 0.001
                grain.velocity[0] *= self.elasticity
            if newy < 0:
                newy = 0
                grain.velocity[1] *= self.elasticity
            elif newy >= self.height:
                newy = self.height - 0.001
                grain.velocity[1] *= self.elasticity

            # old_index/new_index are the prior and new pixel index for this
            # grain -- easier to check motion vs handling X & Y separately.
            old_index = (int(grain.position[1]) * self.width +
                         int(grain.position[0]))
            new_index = int(newy) * self.width + int(newx)

            # If grain's moving to a new pixel, but pixel's already occupied...
            if old_index != new_index and self.get_pixel(newx, newy):
                # What direction when blocked?
                delta = abs(new_index - old_index)
                if delta == 1:                           # 1 pixel left/right
                    newx = grain.position[0]             # Cancel X motion
                    grain.velocity[0] *= self.elasticity # bounce X velocity
                elif delta == self.width:                # 1 pixel up or down
                    newy = grain.position[1]             # Cancel Y motion
                    grain.velocity[1] *= self.elasticity # bounce Y velocity
                else: # Diagonal intersection is more tricky...
                    # Try skidding along just one axis of motion if possible
                    # (start w/faster axis).
                    if abs(grain.velocity[0]) >= abs(grain.velocity[1]):
                        # X axis is faster
                        if not self.get_pixel(newx, grain.position[1]):
                            # (newx, oldy) is free, take it!
                            # But cancel Y motion, bounce Y velocity
                            newy = grain.position[1]
                            grain.velocity[1] *= self.elasticity
                        else: # X pixel is taken, so try Y...
                            if not self.get_pixel(grain.position[0], newy):
                                # (oldx, newy) is free, take it...
                                # but cancel X motion, bounce X velocity
                                newx = grain.position[0]
                                grain.velocity[0] *= self.elasticity
                            else: # Both spots are occupied
                                # Cancel X & Y motion, bounce X & Y velocity
                                newx = grain.position[0]
                                newy = grain.position[1]
                                grain.velocity[0] *= self.elasticity
                                grain.velocity[1] *= self.elasticity
                    else: # Y axis is faster, start there
                        if not self.get_pixel(grain.position[0], newy):
                            # (oldx, newy) is free, take it...
                            # but cancel X motion, bounce X velocity
                            newx = grain.position[0]
                            grain.velocity[0] *= self.elasticity
                        else: # Y pixel is taken, so try X...
                            if not self.get_pixel(newx, grain.position[1]):
                                # (newx, oldy) is free, take it, but...
                                # but cancel Y motion, bounce Y velocity
                                newy = grain.position[1]
                                grain.velocity[1] *= self.elasticity
                            else: # Both spots are occupied
                                # Cancel X & Y motion, bounce X & Y velocity
                                newx = grain.position[0]
                                newy = grain.position[1]
                                grain.velocity[0] *= self.elasticity
                                grain.velocity[1] *= self.elasticity

            # Clear old spot, update grain position, set new spot
            self.clear_pixel(grain.position[0], grain.position[1])
            grain.position[0] = newx
            grain.position[1] = newy
            self.set_pixel(newx, newy)
            



dust = PixelDust(32,32,0.1)

bitmap = displayio.Bitmap(32,32,8)

palette = displayio.Palette(8)

palette[0] = 0x000000
palette[1] = 0xff0000
palette[2] = 0x00ff00
palette[3] = 0x0000ff
palette[4] = 0xffff00
palette[5] = 0xff00ff
palette[6] = 0xff0f0f
palette[7] = 0xffffff

grid = displayio.TileGrid(bitmap,pixel_shader=palette)
group = displayio.Group(scale =4)
group.append(grid)
mc.display.root_group =group

mc.display.brightness=1.0

num_grains=16 
dust.randomize(num_grains)

old_position_x=[0]*num_grains
old_position_y=[0]*num_grains
colorlist=[]

for i in range(num_grains):
    colorlist.append(random.randrange(1,8))
    

def clearOld():
    global old_position_x,old_position_y,num_grains
    for i in range(num_grains):
        bitmap[old_position_x[i], old_position_y[i]]= 0    
    old_position_x=[]
    old_position_y=[]

while True:
    x,y,z = mc.imu.acceleration
    
    if z > 8.0:         
        mc.exit()
        
        
    dust.iterate((-x,y,z))
#     bitmap.fill(0)
    mc.display.auto_refresh=False
    clearOld()
    
    for i in range(num_grains):
        position_x, position_y = dust.get_position(i)
        position_x=int(position_x)
        position_y = int(position_y)
        
        bitmap[position_x, position_y]= colorlist[i]      
        
        old_position_x.append(position_x)
        old_position_y.append(position_y)
         
    mc.display.refresh(target_frames_per_second=60)
    mc.display.auto_refresh=True
 
        
        




