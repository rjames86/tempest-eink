from PIL import Image, ImageDraw, ImageFont

font18 = ImageFont.truetype("./fonts/Font.ttc", 18)
font24 = ImageFont.truetype("./fonts/Font.ttc", 24)
font36 = ImageFont.truetype("./fonts/Font.ttc", 36)
font48 = ImageFont.truetype("./fonts/Font.ttc", 48)
large_icon_font = ImageFont.truetype("./fonts/meteocons.ttf", 72)
medium_icon_font = ImageFont.truetype("./fonts/meteocons.ttf", 36)
small_icon_font = ImageFont.truetype("./fonts/meteocons.ttf", 24)


class Forecasts:
    def __init__(self, image, forecast, observations, rectangle_boundary) -> None:
        self.draw = ImageDraw.Draw(image)

        self.forecast = forecast
        self.observations = observations

        x0, y0, x1, y1 = rectangle_boundary
        self.width = (x1 - x0) // 2
        self.height = y1 - y0

        # Take right half of the rectangle boundary for forecast
        self.x0 = self.width
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1 // 2

        print(self.x0, self.y0, self.x1, self.y1)

        # number of squares we show horizontally
        self.number_squares = 4
        self.square_width = self.width // self.number_squares
        self.square_height = self.height // 2

        self.draw.line([self.x0, self.y1, self.x1, self.y1])

        for i in range(1, self.number_squares):
            self.draw.line(
                [
                    self.x0 + (i * self.square_width),
                    self.y0,
                    self.x0 + (i * self.square_width),
                    self.y1,
                ]
            )

    def draw_forecast(self, i):
        forecast = self.forecast.forecast.hourly[i]
        time = "%s:00" % forecast.local_hour
        font_width, font_height = font18.getsize(time)

        x = (self.width * 5 // 8) - (font_width // 2) + (i * self.square_width)
        y = 10 + self.y0
        self.draw.text([x, y], time, font=font18, fill=0)

        font_width, font_height = medium_icon_font.getsize(forecast.get_icon_letter())

        x = (self.width * 5 // 8) - (font_width // 2) + (i * self.square_width)
        y = 30 + y

        self.draw.text(
            [x, y],
            forecast.get_icon_letter(),
            font=medium_icon_font,
            fill=0,
        )

    def create(self):
        for i in range(self.number_squares):
            self.draw_forecast(i)