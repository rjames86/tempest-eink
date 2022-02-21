from server.config import CONFIG


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

    @staticmethod
    def rainfall(r):
        if CONFIG.units_precip == "in":
            return r * 0.039370078740157
        else:
            return r