from PIL import Image
import pathlib
from os import path

import matplotlib
import numpy as np
from scipy.interpolate import make_interp_spline

from server.config import CONFIG

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator, FuncFormatter
from datetime import datetime

from tempest.observations import get_observations

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

        # Default sizes for when there are 3 charts
        self.chart_width = 2.5
        self.chart_height = 1.75

    def create(self):
        charts = [
            ("Pressure", "Hours", "sea_level_pressure", "line"),
            ("Temperature", "Hours", "air_temperature", "line"),
            ("Humidity", "Hours", "relative_humidity", "line"),
        ]

        # Let's see if there's any rain acumulation. If so, we can add the chart
        print(self.observations.total_rain_acumulation, CONFIG.always_show_rain)
        if self.observations.total_rain_acumulation > 0 or CONFIG.always_show_rain:
            self.chart_width = 2
            charts.append(("Rainfall", CONFIG.units_precip, "rain_accumulation", "bar"))

        x, y = self.start_x + 10, self.start_y + 10
        for i, (y_label, x_label, value, chart_type) in enumerate(charts):
            img = self.create_chart(value, x_label, y_label, chart_type)
            img_width, _ = img.size
            if i == 0:
                x = 0
            else:
                x = x + img_width

            self.image.paste(img, (x, y))

    def create_chart(self, obs_type, x_label_name, y_label_name, chart_type):
        if chart_type == "line":
            return self.create_line_chart(obs_type, x_label_name, y_label_name)
        elif chart_type == "bar":
            return self.create_bar_chart(obs_type, x_label_name, y_label_name)

    def create_line_chart(self, obs_type, x_label_name, y_label_name):
        dates = [obs.time for obs in self.observations]
        temps = [getattr(obs, obs_type) for obs in self.observations]

        x = np.array(dates)
        y = np.array(temps)

        # Returns evenly spaced numbers
        # over a specified interval.
        X_Y_Spline = make_interp_spline(x, y)
        X_ = np.linspace(x.min(), x.max(), 50)
        Y_ = X_Y_Spline(X_)

        fig, ax = plt.subplots(figsize=[self.chart_width, self.chart_height])
        ax.plot(X_, Y_, color="k", markevery=500)
        formatter = get_label(self.observations)
        ax.xaxis.set_major_formatter(FuncFormatter(formatter))
        ax.xaxis.set_major_locator(MaxNLocator(4))

        plt.xlabel("(%s)" % x_label_name, labelpad=0)
        plt.ylabel(y_label_name, rotation=0)
        ax.yaxis.set_label_coords(0.5, 1.02)
        plt.tight_layout()

        fig.savefig(TEMP_FILE)
        pil_img = Image.frombytes(
            "RGB", fig.canvas.get_width_height(), fig.canvas.tostring_rgb()
        )
        return pil_img

    def create_bar_chart(self, obs_type, x_label_name, y_label_name):
        formatter = get_label(self.observations)

        dates = [formatter(obs.time, None) for obs in self.observations]
        temps = [getattr(obs, obs_type) for obs in self.observations]

        fig, ax = plt.subplots(figsize=[self.chart_width, self.chart_height])
        ax.bar(dates, temps, color="k")

        # ax.xaxis.set_major_formatter(FuncFormatter(formatter))
        ax.xaxis.set_major_locator(MaxNLocator(4))

        plt.xlabel("(%s)" % x_label_name, labelpad=0)
        plt.ylabel(y_label_name, rotation=0)
        ax.yaxis.set_label_coords(0.5, 1.02)
        plt.tight_layout()

        fig.savefig(TEMP_FILE)
        pil_img = Image.frombytes(
            "RGB", fig.canvas.get_width_height(), fig.canvas.tostring_rgb()
        )
        return pil_img
