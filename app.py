from tkinter import *
from configparser import ConfigParser
import requests
from tkinter import messagebox

"""
To run this program the api key is required
Assign that api key to key variable in the config.ini file
"""

url="http://api.openweathermap.org/data/2.5/weather?q={}&appid={}"

config_file = "config.ini"
config = ConfigParser()
config.read(config_file)
api_key = config['api_key']['key']


def get_weather(city):
    """
    function used to extract data from the json object
    :param city: name of city such as mumbai, london, etc.
    """

    result = requests.get(url.format(city,api_key))
    if result:
        json = result.json()
        # city , country, temp_celesius, temp_fahrenheit, icon, weather
        city = json['name']
        country = json['sys']['country']
        temp_kelvin = json['main']['temp']
        temp_celsius = temp_kelvin-273.15
        temp_fahrenheit = (temp_kelvin-273.15) * 9/5 + 32
        icon = json['weather'][0]['icon']
        weather = json['weather'][0]['main']
        final = (city, country,temp_celsius, temp_fahrenheit,icon, weather)
        return final
    else:
        return None


def search():
    """
    After hitting search weather button the data generated and put into that respective input field
    """
    city = city_text.get()
    weather = get_weather(city)
    if weather:
        location_label["text"] = "{} {}".format(weather[0], weather[1])
        img["file"] = f'weather_icon/{weather[4]}.png'
        temperature_celcius["text"] = 'Celcius : {:.2f}C'.format(weather[2])
        temperature_fahrenheit["text"] = 'Fahrenheit : {:.2f}f'.format(weather[3])
        weather_lbl["text"] = "Weather: "+weather[5]
    else:
        messagebox.showerror("ERROR", "CAN'T FOUND CITY")

app = Tk()
app.title("WEATHER APP")
app.geometry('400x550')
app.configure(background="black")

city_entry = Label(app, text= "WEATHER APP", font="verdana", fg="Green", bg="cyan")
city_entry.grid(row=0, column=1, padx=(0,120), pady=(20, 35))


city_name_label = Label(app, text= "CITY NAME:", font="arial", fg="Green", bg="yellow")
city_name_label.grid(row=1, column=0, padx=(0,10), pady=(10,0))

city_text = StringVar()
city_entry = Entry(app, textvariable=city_text, font="arial")
city_entry.grid(row=1, column=1, padx=(0,30), pady=(10, 0))

search_btn = Button(app, text="SEARCH WEATHER",font="arial", fg="white", bg="blue", command=search)
search_btn.grid(row=2, column=1, padx= (0,40), pady=(20, 0))


location_label = Label(app, text="", font="arial", fg="White", bg="black")
location_label.grid(row=3, column=1, padx=(0,50), pady=(10, 0))

img = PhotoImage(file='')
weather_Icon = Label(app,image=img)
weather_Icon.grid(row=4, column=1, padx=(0,50), pady=(10, 0))

temperature_celcius = Label(app, text="",font="arial", fg="White", bg="black")
temperature_celcius.grid(row=5, column=1, padx=(0,50), pady=(10, 0))

temperature_fahrenheit = Label(app, text="",font="arial", fg="White", bg="black")
temperature_fahrenheit.grid(row=6, column=1, padx=(0,50), pady=(10, 0))

weather_lbl = Label(app, text="",font="arial", fg="White", bg="black")
weather_lbl.grid(row=7, column=1, padx=(0,50), pady=(10, 0))

exit_btn = Button(app, text="Exit", command=app.quit, font="arial", fg="white", bg="red",padx=100)
exit_btn.grid(row=8, column=1, padx=(0,50), pady=(10, 0))

app.mainloop()

