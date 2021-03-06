from logger import logger

logger.info("Starting up...")

from server.config import CONFIG, config_exists, save_config
from draw_weather import (
    draw_not_configured,
    draw_weather,
)

logger.debug("Finished loading local imports")

import time
from os import environ
from PIL import Image
from datetime import datetime

logger.debug("Finished loading package imports")

testing = environ.get("TESTING", False)
logger.info("is testing: %s" % testing)


class MockEPD:
    width = 800
    height = 480

    def init(self):
        pass

    def Clear(self):
        pass


def get_epd():
    if testing:
        return MockEPD()
    else:
        from waveshare_epd import epd7in5_V2

        return epd7in5_V2.EPD()


def in_between(now, start, end):
    if start <= end:
        return start <= now < end
    else:  # over midnight e.g., 23:30-04:15
        return start <= now or now < end


def main():
    NOW = datetime.now().time()
    logger.info("initializing epd")
    epd = get_epd()
    # Drawing on the Horizontal image
    Himage = Image.new("1", (epd.width, epd.height), 255)  # 255: clear the frame

    if testing:
        config = CONFIG.as_json()
        save_config(config)

        draw_weather(epd, Himage)
        Himage.show()
        return

    try:
        if in_between(NOW, CONFIG.on_time, CONFIG.off_time):
            logger.info("Starting up...")
            
            # Check if config has been set up
            if not config_exists() or CONFIG.token == "":
                epd.init()
                draw_not_configured(epd, Himage)
                epd.Clear()
                epd.display(epd.getbuffer(Himage))
                time.sleep(10)
                epd.sleep()
                return

            config = CONFIG.as_json()
            save_config(config)

            epd.init()
            draw_weather(epd, Himage)
            epd.Clear()
            logger.info("Writing to display...")
            epd.display(epd.getbuffer(Himage))
            time.sleep(10)
            logger.info("Putting screen to sleep....")
            epd.sleep()

        elif not in_between(NOW, CONFIG.on_time, CONFIG.off_time):
            logger.info("Sleeping time. Don't do anything")
            config = CONFIG.as_json()
            save_config(config)
            epd.init()
            epd.Clear()
            epd.sleep()
            return     
        else:
            logger.info("sleeping and already off...")
            return
    except:
        epd.init()
        epd.Clear()
        epd.sleep()


if __name__ == "__main__":
    main()
