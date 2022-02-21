from config import CONFIG, config_exists, save_config
from draw_weather import (
    draw_not_configured,
    draw_weather,
)

import time
from os import environ
from PIL import Image
from datetime import datetime

testing = environ.get("TESTING", False)
print("is testing:", testing)


class MockEPD:
    width = 800
    height = 480

    def init(self):
        pass

    def Clear(self):
        pass

from waveshare_epd import epd7in5_V2

def in_between(now, start, end):
    if start <= end:
        return start <= now < end
    else: # over midnight e.g., 23:30-04:15
        return start <= now or now < end

def main():
    NOW = datetime.now().time()
    # Drawing on the Horizontal image
    Himage = Image.new("1", (epd.width, epd.height), 255)  # 255: clear the frame

    # Check if config has been set up
    if not config_exists() or CONFIG.token == "":
        epd = epd7in5_V2.EPD()
        epd.init()
        draw_not_configured(epd, Himage)
        epd.Clear()
        epd.display(epd.getbuffer(Himage))
        time.sleep(10)
        epd.sleep()
    else:
        if in_between(NOW, CONFIG.on_time, CONFIG.off_time):
            print(NOW, "Starting up...")        

            config = CONFIG.as_json()
            config['is_on'] = True
            save_config(config)

            epd = epd7in5_V2.EPD()
            epd.init()
            draw_weather(epd, Himage)
            epd.Clear()
            epd.display(epd.getbuffer(Himage))
            time.sleep(10)
            epd.sleep()
            
        elif not in_between(NOW, CONFIG.on_time, CONFIG.off_time) and CONFIG.is_on:
            print(NOW, "Sleeping time. Don't do anything")
            config = CONFIG.as_json()
            config['is_on'] = False
            save_config(config)
            epd = epd7in5_V2.EPD()
            epd.init()
            epd.Clear()
            epd.sleep()
            return
        else:
            print(NOW, "sleeping and already off...")
            return

        
if __name__ == "__main__":
    main()
