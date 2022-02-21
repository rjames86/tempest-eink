from config import CONFIG


class Conversions:
    @staticmethod
    def air_temp(temp):
        if CONFIG.units_temp == "f":
            return (temp * 1.8) + 32
        else:
            return temp
