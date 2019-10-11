
# NeoPixel earrings example.  Makes a nice blinky display with just a
# few LEDs on at any time...uses MUCH less juice than rainbow display!

import time

import board
import neopixel
import adafruit_dotstar
import microcontroller

try:
    import urandom as random  # for v1.0 API support
except ImportError:
    import random

dot = adafruit_dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1, brightness=0.2)
dot[0] = (0, 0, 0)

numpix = 16  # Number of NeoPixels (e.g. 16-pixel ring)
pixpin = board.D0  # Pin where NeoPixels are connected
strip = neopixel.NeoPixel(pixpin, numpix, brightness=.3, auto_write=False)

######################### HELPERS ##############################

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (int(255 - pos*3), int(pos*3), 0)
    if pos < 170:
        pos -= 85
        return (0, int(255 - pos*3), int(pos*3))
    pos -= 170
    return (int(pos * 3), 0, int(255 - (pos*3)))

def rainbow_cycle(delay):
    swap = 0
    for j in range(0, 255, 8):  # last digit controls speed of rings
        for i in range(strip.n):
            idx = (i * 256 // strip.n) + j
            if swap > 0:
                strip[i] = wheel(idx & 255)
                swap = 0
            else:
                strip[i] = wheel(256)
                swap += 1
        strip.show()
        time.sleep(delay)

######################### MAIN LOOP ##############################

mode = 1  # Current animation effect
offset = 0  # Position of spinner animation
hue = 120#120 # aquamarine, 880, 1120
color = wheel(hue & 255)  # hue -> RGB color
prevtime = time.monotonic()  # Time of last animation mode switch
######################################
# for pycon
show_blue = True
blue_hue = 160
yellow_hue = 50
color_blue = wheel(blue_hue & 255)
color_yellow = wheel(yellow_hue & 255)
######################################

while True:  # Loop forever...
    if mode in (0, 2, 4):  # Random sparkles - lights just one LED at a time
        i = random.randint(0, numpix - 1)  # Choose random pixel
        ################
        # for pycon
        if show_blue:
            color = color_blue
            show_blue = False
        else:
            color = color_yellow
            show_blue = True
        ################
        strip[i] = color   # Set it to current color
        strip.show()       # Refresh LED states
        # Set same pixel to "off" color now but DON'T refresh...
        # it stays on for now...bot this and the next random
        # pixel will be refreshed on the next pass.
        strip[i] = [0, 0, 0]
        time.sleep(0.008)  # 8 millisecond delay
    elif mode in(1, 3, 5):  # Spinny wheel (4 LEDs on at a time)
        for i in range(numpix):  # For each LED...
            if show_blue:
                color = color_blue
                show_blue = False
            else:
                color = color_yellow
                show_blue = True
            if ((offset + i) & 7) < 2:  # 2 pixels out of 8...
                strip[i] = color    # are set to current color
            else:
                strip[i] = [0, 0, 0]  # other pixels are off
        strip.show()     # Refresh LED states
        time.sleep(0.04) # 40 millisecond delay
        offset += 1      # Shift animation by 1 pixel on next frame
        if offset >= 8:
            offset = 0
    elif mode == 6:
        rainbow_cycle(0.01)
    # Additional animation modes could be added here!

    t = time.monotonic()  # Current time in seconds
    if (t - prevtime) >= 8:  # Every 8 seconds...
        mode += 1  # Advance to next mode
        if mode > 6:  # End of modes?
            mode = 0
        strip.fill([0, 0, 0])  # Turn off all pixels
        prevtime = t  # Record time of last mode change
