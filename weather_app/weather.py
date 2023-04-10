from flask import Flask, request, render_template, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required
import requests
import create_app
from create_app import db, create_app

# db.init_app(app)

main = Blueprint('main', __name__)

@main.route('/current-weather', methods=["GET", "POST"])
@login_required
def index():
    weatherData = ''
    error = 0
    cityName = ''
    if request.method == "POST":
        cityName = request.form.get("cityName")
        tempUnit = request.form.get("tempUnit")
        if cityName:
            weatherApiKey = 'ec51f91c600afa09ead38ae45da2ba11'
            if (tempUnit == "celcius" or tempUnit == "Celcius" or tempUnit == "C"):
                url = "https://api.openweathermap.org/data/2.5/weather?q=" + cityName + "&appid=" + weatherApiKey + "&units=metric"
            elif (tempUnit == "farheneit" or tempUnit == "Farheneit" or tempUnit == "F"):
                url = "https://api.openweathermap.org/data/2.5/weather?q=" + cityName + "&appid=" + weatherApiKey + "&units=imperial"
            else:
                url = "https://api.openweathermap.org/data/2.5/weather?q=" + cityName + "&appid=" + weatherApiKey
            weatherData = requests.get(url).json()
        else:
            error = 1
    return render_template('current_weather.html', data=weatherData, cityName=cityName, error=error)


@main.route('/daily-weather', methods=["GET", "POST"])
@login_required
def daily_weather():
    weatherData = ''
    error = 0
    cityName = ''
    if request.method == "POST":
        cityName = request.form.get("cityName")
        if cityName:
            weatherApiKey = '881ea9b7ab83f037fe4f80745ec90f04'
            url = "https://api.openweathermap.org/data/2.5/forecast?q=" + cityName + "&units=metric&cnt=7&appid=" + weatherApiKey
            weatherData = requests.get(url).json()
        else:
            error = 1
    return render_template('daily_forecast.html', data=weatherData, cityName=cityName, error=error)


@main.route('/fun-facts', methods=["GET", "POST"])
@login_required
def fun_facts():
    return render_template('fun_facts.html')

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run()
