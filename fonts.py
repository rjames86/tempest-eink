import pathlib
from PIL import ImageFont
from os import path

CURRENT_PATH = pathlib.Path(__file__).parent.absolute()
FONT_PATH = path.join(CURRENT_PATH, 'fonts', 'Font.ttc')
ICON_FONT_PATH = path.join(CURRENT_PATH, 'fonts', 'meteocons.ttf')

font12 = ImageFont.truetype(FONT_PATH, 12)
font24 = ImageFont.truetype(FONT_PATH, 24)
font18 = ImageFont.truetype(FONT_PATH, 18)
font36 = ImageFont.truetype(FONT_PATH, 36)
font48 = ImageFont.truetype(FONT_PATH, 48)
font64 = ImageFont.truetype(FONT_PATH, 64)

icon_font = ImageFont.truetype(ICON_FONT_PATH, 48)
large_icon_font = ImageFont.truetype(ICON_FONT_PATH, 72)
medium_icon_font = ImageFont.truetype(ICON_FONT_PATH, 36)
small_icon_font = ImageFont.truetype(ICON_FONT_PATH, 24)