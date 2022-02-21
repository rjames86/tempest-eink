from cgitb import small
from PIL import Image, ImageDraw, ImageFont
import pathlib
from os import path
from fonts import (
    font18,
    font96,
    large_icon_font,
    medium_icon_font,
    small_icon_font,
)

BASE_PATH = pathlib.Path(__file__).parent.parent.absolute()
ARROW_PATH = path.join(BASE_PATH, "images", "cc-pressure-trend-arrow.png")


class CurrentConditions:
    def __init__(self, image, forecast, observations, rectangle_boundary) -> None:
        self.image = image
        self.draw = ImageDraw.Draw(image)

        self.forecast = forecast
        self.observations = observations

        x0, y0, x1, y1 = rectangle_boundary
        # Take left half of the rectangle boundary for current conditions
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1 // 2
        self.y1 = y1

        self.width = x1 - x0
        self.height = y1 - y0

        self.left_center = self.width // 8
        self.right_center = self.width * 3 // 8

        self.draw.rectangle([self.x0, self.y0, self.x1, self.y1], fill=255, outline=0)

    def create(self):
        # left side
        x, y = self.draw_air_temperature(self.left_center, self.y0)
        x, y = self.draw_feels_like(self.left_center, y)
        y += 20  # add some padding between value
        x, y = self.draw_dew_point(self.left_center, y)
        x, y = self.draw_humidity(self.left_center, y)
        x, y = self.draw_pressure(self.left_center, y)

        # right side
        x, y = self.draw_condition_icon(self.right_center, self.y0)
        x, y = self.draw_conditions(self.right_center, y)
        x, y = self.draw_high_lows(self.right_center, y)
        x, y = self.draw_wind(self.right_center, y)
        x, y = self.draw_uv(self.right_center, y)
        x, y = self.draw_sunrise_sunset(self.right_center, y)

    def draw_condition_icon(self, x, y):
        font_width, font_height = large_icon_font.getsize(
            self.forecast.current_conditions.get_icon_letter()
        )

        x = x - (font_width // 2)
        y = (self.height // 8) + y

        self.draw.text(
            [x, y],
            self.forecast.current_conditions.get_icon_letter(),
            font=large_icon_font,
            fill=0,
        )
        return x, y + font_height

    def draw_uv(self, x, y):
        uv = "%s UV" % self.forecast.current_conditions.uv
        text_font_width, text_font_height = font18.getsize(uv)

        text_x = x - (text_font_width // 2)
        text_y = 10 + y

        self.draw.text(
            [text_x, text_y],
            uv,
            font=font18,
            fill=0,
        )

        font_width, font_height = small_icon_font.getsize("B")  # sun

        x = text_x - font_width

        self.draw.text(
            [x, y + (text_font_height // 2)],
            "B",
            font=small_icon_font,
            fill=0,
        )

        return x, y + text_font_height

    def draw_sunrise_sunset(self, x, y):
        today_forcast = self.forecast.forecast.daily[0]

        outer_padding = 30

        black_sun = "1"
        sun_width, sun_height = small_icon_font.getsize(black_sun)
        x = self.width // 4 + outer_padding
        y = y + 20
        self.draw.text(
            [x, y],
            black_sun,
            font=small_icon_font,
            fill=0,
        )

        sunrise = "%s" % today_forcast.sunrise_time
        sunrise_font_width, sunrise_font_height = font18.getsize(sunrise)

        text_x = x + sun_width
        text_y = y

        self.draw.text(
            [text_x, text_y],
            sunrise,
            font=font18,
            fill=0,
        )

        sunset = "%s" % today_forcast.sunset_time
        sunset_font_width, sunset_font_height = font18.getsize(sunset)

        text_x = self.x1 - sunset_font_width - outer_padding
        text_y = y

        self.draw.text(
            [text_x, text_y],
            sunset,
            font=font18,
            fill=0,
        )

        black_moon = "2"
        moon_width, moon_height = small_icon_font.getsize(black_moon)
        x = text_x - moon_width
        self.draw.text(
            [x, y],
            black_moon,
            font=small_icon_font,
            fill=0,
        )

        return x, y + sunrise_font_height

    def draw_conditions(self, x, y):
        conditions = "%s  " % self.forecast.current_conditions.conditions
        font_width, font_height = font18.getsize(conditions)

        x = x - (font_width // 2)
        y = 10 + y

        self.draw.text(
            [x, y],
            conditions,
            font=font18,
            fill=0,
        )
        return x, y + font_height

    def draw_wind(self, x, y):
        wind_text = "%s %s %s" % (
            self.forecast.current_conditions.wind_direction_cardinal,
            self.forecast.current_conditions.wind_avg,
            self.forecast.units.units_wind,
        )
        font_width, font_height = font18.getsize(wind_text)
        x = x - (font_width // 2)
        y = 10 + y

        self.draw.text(
            [x, y],
            wind_text,
            font=font18,
            fill=0,
        )

        wind_direction = self.forecast.current_conditions.wind_direction

        circle_diameter = 24
        circle_radius = circle_diameter // 2
        circle_padding = 10
        circle_coords = [
            x - (circle_diameter + circle_padding),
            y - (circle_radius // 2),
            x - circle_padding,
            y + (circle_diameter - (circle_radius // 2)),
        ]

        # self.draw.ellipse(
        #     circle_coords,
        #     fill=255,
        #     outline=0,
        # )
        # self.draw.pieslice(
        #     circle_coords,
        #     start=-wind_direction - 10,
        #     end=-wind_direction + 10,
        #     fill=0,
        #     outline=0,
        # )

        return x, y + font_height

    def draw_air_temperature(self, x, y):
        air_temp = "%.1f" % (self.forecast.current_conditions.air_temperature)
        font_width, font_height = font96.getsize(air_temp)

        x = x - (font_width // 2)
        y = 20 + y

        self.draw.text([x, y], air_temp, font=font96, fill=0)
        self.draw.text(
            [x + font_width, y + (font_height // 4)],
            self.forecast.units.units_temp_letter(),
            font=medium_icon_font,
            fill=0,
        )
        return x, y + font_height

    def draw_feels_like(self, x, y):
        feels_like_temp = "Feels Like %.0f" % (
            self.forecast.current_conditions.feels_like
        )
        font_width, font_height = font18.getsize(feels_like_temp)

        x = x - (font_width // 2)
        y = 10 + y

        self.draw.text([x, y], feels_like_temp, font=font18, fill=0)
        self.draw.text(
            [x + font_width, y - (font_height // 4)],
            self.forecast.units.units_temp_letter(),
            font=small_icon_font,
            fill=0,
        )
        return x, y + font_height

    def draw_dew_point(self, x, y):
        dew_point_temp = "Dew Point %.1f" % (self.forecast.current_conditions.dew_point)
        font_width, font_height = font18.getsize(dew_point_temp)

        x = x - (font_width // 2)
        y = 10 + y

        self.draw.text([x, y], dew_point_temp, font=font18, fill=0)
        self.draw.text(
            [x + font_width, y - (font_height // 4)],
            self.forecast.units.units_temp_letter(),
            font=small_icon_font,
            fill=0,
        )
        return x, y + font_height

    def draw_high_lows(self, x, y):
        today_forecast = self.forecast.forecast.daily[0]
        high_temp = "H: %.0f L: %.0f" % (
            today_forecast.air_temp_high,
            today_forecast.air_temp_low,
        )
        font_width, font_height = font18.getsize(high_temp)

        x = x - (font_width // 2)
        y = 10 + y

        self.draw.text(
            [x, y],
            high_temp,
            font=font18,
            fill=0,
        )

        return x, y + font_height

    def draw_humidity(self, x, y):
        relative_humidity = "%.0f%% humidity" % (
            self.forecast.current_conditions.relative_humidity
        )
        font_width, font_height = font18.getsize(relative_humidity)

        x = x - (font_width // 2)
        y = 10 + y

        self.draw.text(
            [x, y],
            relative_humidity,
            font=font18,
            fill=0,
        )
        return x, y + font_height

    def draw_pressure(self, x, y):
        sea_level_pressure = "%.3f %s %s" % (
            self.forecast.current_conditions.sea_level_pressure,
            self.forecast.units.units_pressure,
            self.forecast.current_conditions.pressure_trend,
        )
        font_width, font_height = font18.getsize(sea_level_pressure)

        x = x - (font_width // 2)
        y = 10 + y

        self.draw.text(
            [x, y],
            sea_level_pressure,
            font=font18,
            fill=0,
        )
        arrow = Image.open(ARROW_PATH).resize((25, 25))
        arrow_width, arrow_height = arrow.size
        # self.image.paste(arrow, [x - arrow_width, y - (arrow_height // 8)], arrow)
        return x, y + font_height
