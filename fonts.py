import pathlib
from PIL import ImageFont
from os import path

CURRENT_PATH = pathlib.Path(__file__).parent.absolute()
FONT_PATH = path.join(CURRENT_PATH, "fonts")
FONT_FILE = path.join(FONT_PATH, "SourceSansPro-SemiBold.ttf")
ICON_FONT_PATH = path.join(FONT_PATH, "meteocons.ttf")

font12 = ImageFont.truetype(FONT_FILE, 12)
font16 = ImageFont.truetype(FONT_FILE, 16)
font24 = ImageFont.truetype(FONT_FILE, 24)
font18 = ImageFont.truetype(FONT_FILE, 18)
font36 = ImageFont.truetype(FONT_FILE, 36)
font48 = ImageFont.truetype(FONT_FILE, 48)
font64 = ImageFont.truetype(FONT_FILE, 64)

icon_font = ImageFont.truetype(ICON_FONT_PATH, 48)
large_icon_font = ImageFont.truetype(ICON_FONT_PATH, 72)
medium_icon_font = ImageFont.truetype(ICON_FONT_PATH, 36)
small_icon_font = ImageFont.truetype(ICON_FONT_PATH, 24)