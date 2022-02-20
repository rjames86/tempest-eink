from PIL import Image, ImageDraw, ImageFont

font18 = ImageFont.truetype("./fonts/Font.ttc", 18)
font24 = ImageFont.truetype("./fonts/Font.ttc", 24)
font36 = ImageFont.truetype("./fonts/Font.ttc", 36)
font48 = ImageFont.truetype("./fonts/Font.ttc", 48)
large_icon_font = ImageFont.truetype("./fonts/meteocons.ttf", 72)
medium_icon_font = ImageFont.truetype("./fonts/meteocons.ttf", 36)
small_icon_font = ImageFont.truetype("./fonts/meteocons.ttf", 24)


class Forecasts:
    def __init__(self, image, forecast, observations, rectangle_boundary, top_padding) -> None:
        self.draw = ImageDraw.Draw(image)

        self.forecast = forecast
        self.observations = observations

        print(rectangle_boundary)
        x0, y0, x1, y1 = rectangle_boundary
        self.width = x1
        self.height = y1 - y0

        # Take right half of the rectangle boundary for forecast
        self.x0 = self.width // 2
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1 // 2

        # number of squares we show horizontally
        self.number_squares = 4
        self.square_width = self.width // 2 // self.number_squares
        self.square_height = self.height // 2

        self.draw.line([self.x0, self.y1 + self.y0 // 2, self.x1, self.y1+ self.y0 // 2])

        for i in range(1, self.number_squares):
            self.draw.line(
                [
                    self.x0 + (i * self.square_width),
                    self.y0,
                    self.x0 + (i * self.square_width),
                    y1,
                ]
            )

    def draw_forecast(self, i):
        forecast = self.forecast.forecast.hourly[i]

        # draw the time
        time = "%s:00" % forecast.local_hour
        time_font_width, time_font_height = font18.getsize(time)

        x = (self.width * 9 // 16) - (time_font_width // 2) + ((i % self.number_squares) * self.square_width)
        y = 10 + self.y0 + (self.square_height * (i // self.number_squares))

        self.draw.text([x, y], time, font=font18, fill=0)

        # draw weather condition icon
        condition_font_width, condition_font_height = medium_icon_font.getsize(
            forecast.get_icon_letter()
        )

        x = (
            (self.width * 9 // 16)
            - (condition_font_width // 2)
            + ((i % self.number_squares) * self.square_width)
        )
        y = 10 + time_font_height + y
        print('here', i, x, y)

        self.draw.text(
            [x, y],
            forecast.get_icon_letter(),
            font=medium_icon_font,
            fill=0,
        )

        # draw air temperature
        air_temp = "%.1f" % (forecast.air_temperature)
        air_font_width, air_font_height = font18.getsize(air_temp)

        x = (self.width * 9 // 16) - (air_font_width // 2) + ((i % self.number_squares) * self.square_width)
        y = 10 + condition_font_height + y

        self.draw.text([x, y], air_temp, font=font18, fill=0)
        self.draw.text(
            [x + air_font_width, y - (air_font_height // 4)],
            self.forecast.units.units_temp_letter(),
            font=small_icon_font,
            fill=0,
        )

    def create(self):
        for i in range(self.number_squares * 2):
            self.draw_forecast(i)