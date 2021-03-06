from datetime import datetime
import json

import requests
from flask import Flask, redirect, render_template, url_for, jsonify
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import (
    DecimalField,
    SelectField,
    StringField,
    SubmitField,
    TimeField,
    BooleanField,
)
from wtforms.validators import DataRequired

from config import create_or_get_config, save_config, CONFIG

app = Flask(__name__)

app.config["SECRET_KEY"] = "C2HWGVoMGfNTBsrYQg8EcMrdTimkZfAb"
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True

Bootstrap(app)


class TokenForm(FlaskForm):
    token = StringField(
        "Enter Tempest Token",
        description="Create a new token by going to https://tempestwx.com/settings/tokens",
        validators=[DataRequired()],
    )
    submit = SubmitField("Submit")


def create_config_form(config):
    class ConfigForm(FlaskForm):
        on_time = TimeField(
            "Time to turn on", default=datetime.strptime(config["on_time"], "%H:%M")
        )
        off_time = TimeField(
            "Time to turn off", default=datetime.strptime(config["off_time"], "%H:%M")
        )
        include_daily_forecast = BooleanField(
            "Include daily forecast",
            default=config.get("include_daily_forecast", True),
            description="Includes daily forecast along with hourly forecast",
        )
        always_show_rain = BooleanField(
            "Always show rain accumulation chart (If off, it'll only show if there's been rain)",
            default=config.get("always_show_rain", False),
            description="Includes daily forecast along with hourly forecast",
        )
        units_temp = SelectField(
            "Temp Units", default=config["units_temp"], choices=[("f", "F"), ("c", "C")]
        )
        units_wind = SelectField(
            "Wind Units",
            default=config["units_wind"],
            choices=["mph", "kph", "kts", "mps", "bft", "lfm"],
        )
        units_pressure = SelectField(
            "Pressure Units",
            default=config["units_pressure"],
            choices=["mb", "inhg", "mmhg", "hpa"],
        )
        units_precip = SelectField(
            "Precip Units", default=config["units_precip"], choices=["mm", "cm", "in"]
        )
        units_distance = SelectField(
            "Distance Units", default=config["units_distance"], choices=["km", "mi"]
        )
        elevation = DecimalField(
            "Current Elevation (meters)", default=config["elevation"], places=10
        )
        submit = SubmitField("Submit")

    return ConfigForm()


def get_station_data(token):
    try:
        resp = requests.get(
            "https://swd.weatherflow.com/swd/rest/stations", params=dict(token=token)
        ).json()

        if "status" in resp and resp["status"]["status_code"] != 0:
            return 500, None

        # Just going to assume there's only ever one
        station = resp["stations"][0]
        data = {
            "token": token,
            "elevation": station["station_meta"]["elevation"],
            "station_id": station["station_id"],
            "station_name": station["name"],
        }

        for device in station["devices"]:
            if device["device_type"] == "ST":
                data["device_id"] = device["device_id"]

        return 200, data

    except Exception:
        return 500, None


@app.route("/", methods=["GET", "POST"])
def index():
    config = create_or_get_config()

    form = TokenForm()
    config_form = create_config_form(config)
    message = ""
    if form.validate_on_submit():
        token = form.token.data
        status_code, station_info = get_station_data(token)
        if status_code != 200:
            message = "Error. Token may be invalid"
        else:
            config.update(station_info)
            save_config(config)
        return render_template(
            "index.html",
            form=form,
            message="hello world",
            config=config,
            config_form=create_config_form(config),
        )

    if config_form.validate_on_submit():
        config.update(
            dict(
                on_time=config_form.on_time.data.strftime("%H:%M"),
                off_time=config_form.off_time.data.strftime("%H:%M"),
                units_temp=config_form.units_temp.data,
                units_wind=config_form.units_wind.data,
                units_pressure=config_form.units_pressure.data,
                units_precip=config_form.units_precip.data,
                units_distance=config_form.units_distance.data,
                elevation=float(config_form.elevation.data),
                include_daily_forecast=config_form.include_daily_forecast.data,
                always_show_rain=config_form.always_show_rain.data,
            )
        )
        print(config)
        save_config(config)
        return render_template(
            "index.html",
            form=form,
            message="hello world",
            config=config,
            config_form=create_config_form(config),
        )
    return render_template(
        "index.html",
        form=form,
        message="hello world",
        config=config,
        config_form=config_form,
    )


@app.route("/config/show", methods=["GET"])
def show_config():
    create_or_get_config()
    return jsonify(CONFIG.as_json())


@app.route("/config/delete", methods=["POST"])
def delete_config():
    create_or_get_config(recreate=True)
    return redirect(url_for("index"))


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500
