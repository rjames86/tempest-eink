from tempest.forecast import get_forecast
from tempest.observations import get_observations
from draw_weather.current_conditions import CurrentConditions

forecast = get_forecast()
observations = get_observations()

datas = [
    forecast.current_conditions.conditions,
    forecast.current_conditions.icon,
    forecast.current_conditions.air_temperature,
    forecast.current_conditions.sea_level_pressure,
    forecast.current_conditions.pressure_trend,
    forecast.current_conditions.relative_humidity,
    forecast.current_conditions.wind_direction,
    forecast.current_conditions.wind_direction_cardinal,
    "-----",
    observations,
]

from waveshare_epd import epd7in5_V2
import time
from PIL import Image, ImageDraw, ImageFont
import logging

logging.info("epd7in5_V2 Demo")
epd = epd7in5_V2.EPD()

logging.info("init and Clear")
epd.init()
epd.Clear()

font24 = ImageFont.truetype("./fonts/Font.ttc", 24)
font18 = ImageFont.truetype("./fonts/Font.ttc", 18)
font36 = ImageFont.truetype("./fonts/Font.ttc", 36)
font48 = ImageFont.truetype("./fonts/Font.ttc", 48)
icon_font = ImageFont.truetype("./fonts/meteocons.ttf", 48)

# Drawing on the Horizontal image
logging.info("1.Drawing on the Horizontal image...")
Himage = Image.new("1", (epd.width, epd.height), 255)  # 255: clear the frame
draw = ImageDraw.Draw(Himage)

# # Create the bounding box for current conditions
side_padding = 5
top_padding = 30
x0, y0 = (0 + side_padding), (0 + top_padding)
x1, y1 = (epd.width - side_padding), ((epd.height - top_padding) * 2 // 3)

full_rect = [x0, y0, x1, y1]
half_rect = [x0, y0, x1 // 2, y1]
quarter_rect = [x0, y0, x1 // 4, y1]

draw.rectangle(full_rect, fill=255, outline=0)

c = CurrentConditions(
    Himage,
    forecast,
    observations,
    full_rect,
)
c.create()

epd.display(epd.getbuffer(Himage))

time.sleep(60 * 3)
epd.Clear()
