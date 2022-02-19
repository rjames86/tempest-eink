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
font36 = ImageFont.truetype("./fonts/Font.ttc", 36)
font48 = ImageFont.truetype("./fonts/Font.ttc", 48)
icon_font = ImageFont.truetype("./fonts/meteocons.ttf", 48)

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
top_padding = 30
x0, y0 = (0 + side_padding), (0 + top_padding)
x1, y1 = (epd.width - side_padding), ((epd.height - top_padding) * 2 // 3)

full_rect = [x0, y0, x1, y1]
half_rect = [x0, y0, x1 // 2, y1]
quarter_rect = [x0, y0, x1 // 4, y1]

draw.rectangle(full_rect, fill=255, outline=0)
draw.rectangle(half_rect, fill=255, outline=0)
draw.rectangle(quarter_rect, fill=255, outline=0)


# Draw Air temperature
air_temp = "%.1f" % (forecast.current_conditions.air_temperature)
font_width, font_height = font48.getsize(air_temp)
draw.text(
    (((x1 - x0) // 8) - (font_width // 2), top_padding + 10),
    air_temp,
    font=font48,
    fill=0,
)
draw.text(
    (((x1 - x0) // 8) + (font_width // 2), top_padding + 10),
    forecast.units.units_temp_letter(),
    font=icon_font,
    fill=0,
)

# Draw feels like
feels_like_temp = "Feels Like %.0f" % (forecast.current_conditions.feels_like)
font_width, font_height = font18.getsize(feels_like_temp)
draw.text(
    (((x1 - x0) // 8) - (font_width // 2), top_padding + 70),
    feels_like_temp,
    font=font18,
    fill=0,
)

# Draw Humidity
relative_humidity = "%.0f humidity" % (forecast.current_conditions.relative_humidity)
font_width, font_height = font18.getsize(relative_humidity)
draw.text(
    (((x1 - x0) // 8) - (font_width // 2), top_padding + 140),
    relative_humidity,
    font=font18,
    fill=0,
)

# Draw Pressure
sea_level_pressure = "%.1f %% %s" % (
    forecast.current_conditions.sea_level_pressure,
    forecast.units.units_pressure,
)
font_width, font_height = font18.getsize(sea_level_pressure)
draw.text(
    (((x1 - x0) // 8) - (font_width // 2), top_padding + 180),
    sea_level_pressure,
    font=font18,
    fill=0,
)


# Draw Condition icon
icon_font_width, icon_font_height = font48.getsize(
    forecast.current_conditions.get_icon_letter()
)
draw.text(
    (((x1 - x0) * 3 // 8) - (icon_font_width // 2), top_padding + 10),
    forecast.current_conditions.get_icon_letter(),
    font=icon_font,
    fill=0,
)

# Draw conditions
conditions = forecast.current_conditions.conditions
font_width, font_height = font18.getsize(conditions)
draw.text(
    (((x1 - x0) * 3 // 8) - (font_width // 2), top_padding + icon_font_height + 20),
    conditions,
    font=font18,
    fill=0,
)

# Draw wind and direction
wind_direction = forecast.current_conditions.wind_direction
wind_direction_icon = Image.open("./images/cc-wind.png")
wind_text = "%s %s %s" % (
    forecast.current_conditions.wind_direction_cardinal,
    forecast.current_conditions.wind_avg,
    forecast.units.units_wind,
)
font_width, font_height = font18.getsize(wind_text)
rotated_wind_direction_icon = wind_direction_icon.rotate(wind_direction)
draw.text(
    (((x1 - x0) * 3 // 8) - (font_width // 2), top_padding + 140),
    conditions,
    font=font18,
    fill=0,
)
Himage.paste(
    rotated_wind_direction_icon, (((x1 - x0) * 3 // 8) - font_width, top_padding + 140)
)


epd.display(epd.getbuffer(Himage))

time.sleep(60 * 3)
epd.Clear()
