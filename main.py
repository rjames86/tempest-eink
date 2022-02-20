from tempest.forecast import get_forecast
from tempest.observations import get_observations
from draw_weather.current_conditions import CurrentConditions
from draw_weather.forecasts import Forecasts
from draw_weather.charts import Charts

import time
from os import environ
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import logging

testing = environ.get("TESTING", False)
print("is testing:", testing)


class MockEPD:
    width = 800
    height = 480

    def init(self):
        pass

    def Clear(self):
        pass


if not testing:
    from waveshare_epd import epd7in5_V2

    epd = epd7in5_V2.EPD()
else:
    epd = MockEPD()

font12 = ImageFont.truetype("./fonts/Font.ttc", 12)
font24 = ImageFont.truetype("./fonts/Font.ttc", 24)
font18 = ImageFont.truetype("./fonts/Font.ttc", 18)
font36 = ImageFont.truetype("./fonts/Font.ttc", 36)
font48 = ImageFont.truetype("./fonts/Font.ttc", 48)
icon_font = ImageFont.truetype("./fonts/meteocons.ttf", 48)


def main():
    forecast = get_forecast()
    observations = get_observations()

    epd.init()
    # Drawing on the Horizontal image
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

    # We create the charts before anything else. Since there's
    # some weird padding issues, I want the rectangle to draw
    # over the images
    charts = Charts(Himage, observations, 0, y1)
    charts.create()

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    draw.text((5, 5), "Last updated: %s   " % now, font=font12, fill=0)
    draw.rectangle(full_rect, fill=255, outline=0)

    c = CurrentConditions(
        Himage,
        forecast,
        observations,
        full_rect,
    )
    c.create()

    f = Forecasts(
        Himage,
        forecast,
        observations,
        full_rect,
        top_padding,
    )
    f.create()

    if not testing:
        if datetime.now().strftime("%H") == "13":
            print("Clearing screen to avoid burn in")
            epd.Clear()

        epd.display(epd.getbuffer(Himage))
        time.sleep(10)
        epd.sleep()
        print("sleeping for 2 minutes")
        time.sleep(60 * 2)
    else:
        Himage.show()


if __name__ == "__main__":
    while True:
        print("Running...")
        main()