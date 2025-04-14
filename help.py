import sys
import os
import epaper
import time
from PIL import Image, ImageDraw, ImageFont

#sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../lib'))
#from waveshare_epd import epd7in5
print("before try block")
try:
    # Init and clear
    epd = epaper.epaper('epd7in5').EPD()
    epd.init()
#    epd.Clear()

    print("initialized")
    
    # Create image canvas
    image = Image.new('1', (epd.width, epd.height), 255)
    draw = ImageDraw.Draw(image)

    print("about to load font and draw!")

    # Load a font and draw text
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 48)
    draw.text((100, 200), "Hello, World!", font=font, fill=0)

    print("drew!")

    # Display the image
    epd.display(epd.getbuffer(image))
    #epd.sleep()

    print("display done")
    
except Exception as e:
    print("Error:", e)
