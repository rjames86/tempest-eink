from PIL.ImageDraw import ImageDraw

from logger import logger

class Draw(ImageDraw):
	def __init__(self, im, mode=None):
		super().__init__(im, mode)
		
	def text(
		self,
		xy,
		text,
		fill=None,
		font=None,
		anchor=None,
		spacing=4,
		align="left",
		direction=None,
		features=None,
		language=None,
		stroke_width=0,
		stroke_fill=None,
		embedded_color=False,
		*args,
		**kwargs,
	):
		try:
			super().text(
				xy,
				text,
				fill,
				font,
				anchor,
				spacing,
				align,
				direction,
				features,
				language,
				stroke_width,
				stroke_fill,
				embedded_color,
				*args,
				**kwargs,
			)
		except:
			logger.error("Failed to draw: %s" % text)
			super().text(
				xy,
				'N/A',
				fill,
				font,
				anchor,
				spacing,
				align,
				direction,
				features,
				language,
				stroke_width,
				stroke_fill,
				embedded_color,
				*args,
				**kwargs,
			) 
	
	def rectangle(self, xy, fill=None, outline=None, width=1):
		try:
			super().rectangle(xy, fill, outline, width)
		except:
			pass