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

        self.width = x1 - x0
        self.height = y1 - y0

        x0, y0, x1, y1 = rectangle_boundary
        # Take half of the rectangle boundary for current conditions
        self.x0 = self.width / 2
        self.y0 = y0
        self.x1 = self.width
        self.y1 = y1 / 2

        # number of squares we show horizontally
        self.number_squares = 4
        self.square_width = self.width / self.number_squares
        self.square_height = self.height / 2

        for i in range(self.number_squares):
            x0, y0 = [i * self.square_width, self.y0]
            x1, y1 = [2 * i * self.square_width, self.square_height]
            self.draw.rectangle([self.x0, y0, self.x1, self.y1], fill=255, outline=0)

    def create(self):
        pass