from PIL import Image, ImageDraw, ImageFont

font18 = ImageFont.truetype("./fonts/Font.ttc", 18)
font24 = ImageFont.truetype("./fonts/Font.ttc", 24)
font36 = ImageFont.truetype("./fonts/Font.ttc", 36)
font48 = ImageFont.truetype("./fonts/Font.ttc", 48)
icon_font = ImageFont.truetype("./fonts/meteocons.ttf", 54)


class CurrentConditions:
    def __init__(self, image, forecast, observations, rectangle_boundary) -> None:
        self.draw = ImageDraw.Draw(image)

        self.forecast = forecast
        self.observations = observations

        x0, y0, x1, y1 = rectangle_boundary
        # Take half of the rectangle boundary for current conditions
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1 // 2
        self.y1 = y1

        self.width = x1 - x0
        self.height = y1 - y0

        self.draw.rectangle([self.x0, self.y0, self.x1, self.y1], fill=255, outline=0)

    def create(self):
        # left side
        x, y = self.draw_air_temperature(self.x0, self.y0)
        x, y = self.draw_feels_like(x, y)
        x, y = self.draw_humidity(x, y)
        x, y = self.draw_pressure(x, y)

        # right side
        x, y = self.draw_condition_icon(self.x0, self.y0)
        x, y = self.draw_conditions(x, y)
        x, y = self.draw_wind(x, y)

    def draw_condition_icon(self, x, y):
        font_width, font_height = font48.getsize(
            self.forecast.current_conditions.get_icon_letter()
        )

        x = (self.width * 3 // 8) - (font_width // 2)
        y = 10 + y

        self.draw.text(
            [x, y],
            self.forecast.current_conditions.get_icon_letter(),
            font=icon_font,
            fill=0,
        )
        return x, y + font_height

    def draw_conditions(self, x, y):
        conditions = self.forecast.current_conditions.conditions
        font_width, font_height = font18.getsize(conditions)

        x = (self.width * 3 // 8) - (font_width // 2)
        y = 20 + y

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
        x = (self.width * 3 // 8) - (font_width // 2)
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

        self.draw.ellipse(
            circle_coords,
            fill=255,
            outline=0,
        )
        self.draw.pieslice(
            circle_coords,
            start=-wind_direction - 10,
            end=-wind_direction + 10,
            fill=0,
            outline=0,
        )

        return x, y + font_height

    def draw_air_temperature(self, x, y):
        air_temp = "%.1f" % (self.forecast.current_conditions.air_temperature)
        font_width, font_height = font48.getsize(air_temp)

        x = (self.width // 8) - (font_width // 2)
        y = 10 + y

        self.draw.text([x, y], air_temp, font=font48, fill=0)
        self.draw.text(
            [x + font_width, y],
            self.forecast.units.units_temp_letter(),
            font=icon_font,
            fill=0,
        )
        return x, y + font_height

    def draw_feels_like(self, x, y):
        feels_like_temp = "Feels Like %.0f" % (
            self.forecast.current_conditions.feels_like
        )
        font_width, font_height = font18.getsize(feels_like_temp)

        x = (self.width // 8) - (font_width // 2)
        y = 10 + y

        self.draw.text([x, y], feels_like_temp, font=font18, fill=0)
        return x, y + font_height

    def draw_humidity(self, x, y):
        relative_humidity = "%.0f humidity" % (
            self.forecast.current_conditions.relative_humidity
        )
        font_width, font_height = font18.getsize(relative_humidity)

        x = (self.width // 8) - (font_width // 2)
        y = 40 + y

        self.draw.text(
            [x, y],
            relative_humidity,
            font=font18,
            fill=0,
        )
        return x, y + font_height

    def draw_pressure(self, x, y):
        sea_level_pressure = "%.1f %% %s" % (
            self.forecast.current_conditions.sea_level_pressure,
            self.forecast.units.units_pressure,
        )
        font_width, font_height = font18.getsize(sea_level_pressure)

        x = (self.width // 8) - (font_width // 2)
        y = 10 + y

        self.draw.text(
            [x, y],
            sea_level_pressure,
            font=font18,
            fill=0,
        )
        return x, y + font_height