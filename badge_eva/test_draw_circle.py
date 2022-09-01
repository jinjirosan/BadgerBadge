import badger2040
import badger_os
import time
import math
import gfx

WIDTH = badger2040.WIDTH # 296
HEIGHT = badger2040.HEIGHT # 128

# Create a new Badger and set it to update FAST
display = badger2040.Badger2040()
graphics = gfx.GFX(296, 128, display.pixel)
display.led(128)

#display.font("bitmap8")

display.update_speed(badger2040.UPDATE_FAST) # first draw is normal to get everything nice and sharp

display.pen(0)    
display.thickness(2) # nice fat pie and lines
display.pen(0) # use pen(12) for spent slice, pen(0) for full slice
graphics.fill_triangle(246, 93, 266, 83, 266, 103) # 6 fill
display.pen(15)
graphics.triangle(246, 93, 266, 83, 266, 103) # 6 outline +200x
display.pen(0) # use pen(12) for spent slice, pen(0) for full slice
graphics.fill_triangle(246, 113, 246, 93, 266, 103) # 5 fill +200x
display.pen(15)
graphics.triangle(246, 113, 246, 93, 266, 103) # 5 outline +200x
display.pen(0) # use pen(12) for spent slice, pen(0) for full slice
graphics.fill_triangle(266, 123, 246, 113, 266, 103) # 4 fill +200x
display.pen(15)
graphics.triangle(266, 123, 246, 113, 266, 103) # 4 outline
display.pen(0) # use pen(12) for spent slice, pen(0) for full slice
graphics.fill_triangle(286, 113, 266, 123, 266, 103) # 3 fill +200x
display.pen(15)
graphics.triangle(286, 113, 266, 123, 266, 103) # 3 outline +200x
display.pen(0) # use pen(12) for spent slice, pen(0) for full slice
graphics.fill_triangle(286, 93, 286, 113, 266, 103) # 2 fill
display.pen(15)
graphics.triangle(286, 93, 286, 113, 266, 103) # 2 outline +200x
display.pen(0) # use pen(12) for spent slice, pen(0) for full slice
graphics.fill_triangle(266, 83, 286, 93, 266, 103) # 1 fill +200x
display.pen(15)
graphics.triangle(266, 83, 286, 93, 266, 103) # 1 outline +200x

display.pen(0)
display.thickness(2) # nice fat pie and lines
graphics.circle(47, 22, 20) # red outline
graphics.fill_circle(47, 22, 15) # red fill
display.pen(15) # disable for non-fill letter
display.font("sans")
display.thickness(1)
display.text("R", 40, 22, 0.7)

display.pen(0)
display.thickness(2) # nice fat pie and lines
graphics.circle(47, 64, 20) # orange outline
#graphics.fill_circle(47, 64, 15) # orange fill
#display.pen(15) # disable for non-fill letter
display.font("sans")
display.thickness(1)
display.text("O", 40, 64, 0.7)

display.pen(0)
display.thickness(2) # nice fat pie and lines
graphics.circle(47, 106, 20) # green outline
#graphics.fill_circle(47, 106, 15) # green fill
#display.pen(15) # disable for non-fill letter
display.font("sans")
display.thickness(1)
display.text("G", 40, 105, 0.7)

display.update()
display.led(0)