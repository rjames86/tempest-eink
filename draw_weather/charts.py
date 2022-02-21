from tracemalloc import start
from PIL import Image
import pathlib
from os import path

import matplotlib
from matplotlib import font_manager

from fonts import FONT_PATH, FONT_FILE

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator, FuncFormatter
from datetime import datetime

from tempest.observations import get_observations

# Add every font at the specified location
for font in font_manager.findSystemFonts([FONT_PATH]):
    font_manager.fontManager.addfont(font)

# Set font family globally
plt.rcParams["font.family"] = "Source Sans Pro"

CURRENT_PATH = pathlib.Path(__file__).parent.parent.absolute()
TEMP_FILE = path.join(CURRENT_PATH, "temp", "temp.png")


def convert_to_hours(delta):
    total_seconds = delta.total_seconds()
    hours = str(int(total_seconds // 3600))
    return f"{hours}"


def get_label(obs):
    def _get_label(tick_val, tick_pos):
        start_time = datetime.fromtimestamp(tick_val)
        end_time = obs[-1].timestamp
        return convert_to_hours((end_time - start_time))

    return _get_label


class Charts:
    def __init__(self, image, observations, start_x, start_y):
        self.image = image
        self.observations = observations
        self.start_x = start_x
        self.start_y = start_y

    def create(self):
        charts = [
            ("Pressure", "sea_level_pressure"),
            ("Temperature", "air_temperature"),
            ("Humidity", "relative_humidity"),
        ]
        x, y = self.start_x + 10, self.start_y + 10
        for i, (label, value) in enumerate(charts):
            img = self.create_chart(value, label)
            img_width, _ = img.size
            if i == 0:
                x = 0
            else:
                x = x + img_width + 5

            self.image.paste(img, (x, y))

    def create_chart(self, obs_type, y_label_name):
        dates = [obs.time for obs in self.observations]
        temps = [getattr(obs, obs_type) for obs in self.observations]

        fig, ax = plt.subplots(figsize=[2.5, 1.75])
        ax.plot(dates, temps, color="k")
        formatter = get_label(self.observations)
        ax.xaxis.set_major_formatter(FuncFormatter(formatter))
        ax.xaxis.set_major_locator(MaxNLocator(4))

        plt.xlabel("(Hours)", labelpad=0)
        plt.ylabel(y_label_name, rotation=0)
        ax.yaxis.set_label_coords(0.5, 1.02)
        plt.tight_layout()

        fig.savefig(TEMP_FILE)

        # open image as PIL object
        img = Image.open(TEMP_FILE)
        pil_img = Image.frombytes(
            "RGB", fig.canvas.get_width_height(), fig.canvas.tostring_rgb()
        )
        return pil_img
