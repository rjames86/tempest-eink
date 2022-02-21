from config import CONFIG


class Conversions:
    @staticmethod
    def air_temp(temp):
        if CONFIG.units_temp == "f":
            return (temp * 1.8) + 32
        else:
            return temp

    @staticmethod
    def pressure(p):
        if CONFIG.units_pressure == "inhg":
            return p * 0.029529980164712
        else:
            return p