from PIL import Image, ImageOps
from PIL import ImageFont
from PIL import ImageDraw

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MaxNLocator
from datetime import timedelta

from tempest.observations import get_observations

def create_chart():
    observations = get_observations("obs_st")
    print(len(observations))
    dates = [i / 60 for i in range(len(observations))]
    temps = [obs.air_temperature for obs in observations]

    fig, ax = plt.subplots()
    ax.plot(dates, temps)
    # ax.xaxis_date()

    formatter = mdates.DateFormatter("%b %d %H:%M")
    # ax.xaxis.set_major_formatter(formatter)
    ax.xaxis.set_major_locator(MaxNLocator(3)) 

    # fig.autofmt_xdate()
    fig.savefig("./temp.png")

    # open image as PIL object
    img = Image.open("./temp.png")
    # pil_img = Image.frombytes(
    #     "RGB", fig.canvas.get_width_height(), fig.canvas.tostring_rgb()
    # )
    pil_img = Image.frombytes(
        "RGB", fig.canvas.get_width_height(), fig.canvas.tostring_rgb()
    )
    pil_img.show()
    return pil_img

create_chart()