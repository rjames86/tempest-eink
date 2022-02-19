from tempest.forecast import get_forecast
from tempest.observations import get_observations

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

# Drawing on the Horizontal image
logging.info("1.Drawing on the Horizontal image...")
Himage = Image.new("1", (epd.width, epd.height), 255)  # 255: clear the frame
draw = ImageDraw.Draw(Himage)
# draw.text((10, 0), "%s" % forecast.current_conditions.conditions, font=font24, fill=0)
# draw.text(
#     (50, 20), "%s" % forecast.current_conditions.air_temperature, font=font24, fill=0
# )
# draw.text(
#     (100, 0), "%s" % forecast.current_conditions.wind_direction, font=font24, fill=0
# )

# Create the bounding box for current conditions
side_padding = 5
top_padding = 10
x0, y0 = (0 + side_padding), (0 + top_padding)
x1, y1 = (epd.width - side_padding), (epd.height // 3)

draw.rectangle([x0, y0, x1, y1], fill=255, outline=0)
draw.text(
    (side_padding + 5, top_padding + 10),
    "Conditions: %s" % forecast.current_conditions.conditions,
    font=font24,
    fill=0,
)


epd.display(epd.getbuffer(Himage))
time.sleep(15)

epd.Clear()
