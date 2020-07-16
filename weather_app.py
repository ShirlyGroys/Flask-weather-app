from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/')
def welcome():
    return f'Welcome to weather app'

@app.route('/city')
def search_city():
    API_KEY = request.args.get('API_KEY')  # add your key here
    city = request.args.get('city')

    # checks if API_KEY and city exists
    if not API_KEY:
        return f'no API_key parameter found'
    if not city:
        return f'no city parameter found'

    # create api requests
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={API_KEY}'
    response = requests.get(url).json()

    # checking for parameter's error
    if response.get('cod') != 200:
        message = response.get('message', '')
        return f'cant get temperature for {city.title()}. Error message = {message}'

    # converting temperature to celsius
    current_temperature = response.get('main', {}).get('temp')
    if current_temperature:
        current_temperature_celsius = round(current_temperature - 273.15, 2)
        weather_data = []
        weather = {
            'city' : response.get('name'),
            'temperature' :current_temperature_celsius,
            'description' : response['weather'][0]['description'],
            'icon' : response['weather'][0]['icon'],
        }
        weather_data.append(weather)
    else:
        return f'cant get temperature for {city.title()}'


    return render_template('weather.html', weather_data=weather_data)



if __name__ == '__main__':
    app.run(debug=True)


