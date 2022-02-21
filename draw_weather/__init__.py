from PIL import ImageDraw
from datetime import datetime
from dateutil import tz

from tempest.forecast import get_forecast
from tempest.observations import get_observations
from draw_weather.current_conditions import CurrentConditions
from draw_weather.forecasts import Forecasts
from draw_weather.charts import Charts
from fonts import (
    font16,
    font24,
    font48,
)


def draw_not_configured(epd, image):
    draw = ImageDraw.Draw(image)

    text = "Tempest Weatherflow"
    font_width, font_height = font48.getsize(text)
    draw.text([epd.width // 2 - (font_width // 2), 0], text, font=font48, fill=0)

    text = "Token not set. Visit http://tempest-eink.local to set up"
    font_width, _ = font24.getsize(text)
    draw.text(
        [epd.width // 2 - (font_width // 2), font_height + 10],
        text,
        font=font24,
        fill=0,
    )


def draw_weather(epd, image):
    draw = ImageDraw.Draw(image)

    forecast = get_forecast()
    observations = get_observations()

    # Create the bounding box for current conditions
    side_padding = 5
    top_padding = 30
    x0, y0 = (0 + side_padding), (0 + top_padding)
    x1, y1 = (epd.width - side_padding), ((epd.height - top_padding) * 2 // 3)

    full_rect = [x0, y0, x1, y1]

    # We create the charts before anything else. Since there's
    # some weird padding issues, I want the rectangle to draw
    # over the images
    charts = Charts(image, observations, 0, y1)
    charts.create()

    now = datetime.now(tz=tz.gettz("America/Denver")).strftime("%Y-%m-%d %H:%M:%S")
    draw.text((5, 5), "Last updated: %s   " % now, font=font16, fill=0)
    draw.rectangle(full_rect, fill=255, outline=0)

    c = CurrentConditions(
        image,
        forecast,
        observations,
        full_rect,
    )
    c.create()

    f = Forecasts(
        image,
        forecast,
        observations,
        full_rect,
        top_padding,
    )
    f.create()