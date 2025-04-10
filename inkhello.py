import time
import digitalio
import busio
import board
from PIL import Image, ImageDraw, ImageFont
from adafruit_epd.il0398 import Adafruit_IL0398  # Driver for 800x480 BW display
from adafruit_epd.epd import Adafruit_EPD

# Display resolution for 7.5" BW E-Ink
EPD_WIDTH = 800
EPD_HEIGHT = 480

# Color constants for 1-bit display
WHITE = 1
BLACK = 0

# Layout constants
BORDER = 30
FONTSIZE = 48
BACKGROUND_COLOR = WHITE
FOREGROUND_COLOR = BLACK
TEXT_COLOR = WHITE

# SPI and pin setup
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
ecs = digitalio.DigitalInOut(board.CE0)     # Chip select
dc = digitalio.DigitalInOut(board.D25)      # Data/command
rst = digitalio.DigitalInOut(board.D17)     # Reset
busy = digitalio.DigitalInOut(board.D24)    # Busy
srcs = None

# Initialize the display
display = Adafruit_IL0398(
    EPD_WIDTH, EPD_HEIGHT, spi,
    cs_pin=ecs,
    dc_pin=dc,
    sramcs_pin=srcs,
    rst_pin=rst,
    busy_pin=busy
)
display.rotation = 1  # Rotate as needed (0–3)

# Create a 1-bit image canvas
image = Image.new("1", (display.width, display.height))
draw = ImageDraw.Draw(image)

# Fill background
draw.rectangle((0, 0, display.width, display.height), fill=BACKGROUND_COLOR)

# Draw inner black rectangle
draw.rectangle(
    (BORDER, BORDER, display.width - BORDER - 1, display.height - BORDER - 1),
    fill=FOREGROUND_COLOR,
)

# Load font
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", FONTSIZE)

# Draw centered text
text = "Hello 7.5\" E-Ink!"
font_width, font_height = font.getsize(text)
text_x = (display.width - font_width) // 2
text_y = (display.height - font_height) // 2
draw.text((text_x, text_y), text, font=font, fill=TEXT_COLOR)

# Show the image on the display
display.image(image)
display.display()

# Keep on screen for 3 minutes
time.sleep(180)

# Clear the display to all white
draw.rectangle((0, 0, display.width, display.height), fill=WHITE)
display.image(image)
display.display()
