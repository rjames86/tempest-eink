from PIL import Image, ImageDraw, ImageFont

font18 = ImageFont.truetype("./fonts/Font.ttc", 18)
font24 = ImageFont.truetype("./fonts/Font.ttc", 24)
font36 = ImageFont.truetype("./fonts/Font.ttc", 36)
font48 = ImageFont.truetype("./fonts/Font.ttc", 48)
icon_font = ImageFont.truetype("./fonts/meteocons.ttf", 48)


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
        x, y = self.draw_air_temperature(self.x0, self.y0)
        x, y = self.draw_humidity(x, y)
        x, y = self.draw_pressure(x, y)

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

    def draw_humidity(self, x, y):
        relative_humidity = "%.0f humidity" % (
            self.forecast.current_conditions.relative_humidity
        )
        font_width, font_height = font18.getsize(relative_humidity)

        x = (self.width // 8) - (font_width // 2)
        y = 10 + y

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