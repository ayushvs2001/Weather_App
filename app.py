from tkinter import *
from configparser import ConfigParser
import requests
from tkinter import messagebox
from tkinter import ttk
import sqlite3
from datetime import datetime

"""
To run this program the api key is required
Assign that api key to key variable in the config.ini file
"""

url="http://api.openweathermap.org/data/2.5/weather?q={}&appid={}"

config_file = "config.ini"
config = ConfigParser()
config.read(config_file)
api_key = config['api_key']['key']

def add(final):
    # create a database or connect to one
    conn = sqlite3.connect("weather_database.db")
    # create cursor
    c = conn.cursor()

    now = datetime.now()
    current_date = now.date()
    current_time = now.strftime("%H:%M:%S")

    c.execute("INSERT INTO weather_info VALUES (:city_name, :country_name, :temp_celcius, :temp_fahrenheit, :weather, :date, :time)",
              {
                  "city_name": final[0],
                   "country_name":  final[1],
                   "temp_celcius":  "{:.2f}".format(final[2]),
                   "temp_fahrenheit":   "{:.2f}".format(final[3]),
                   "weather":   final[5],
                   "date":  current_date,
                   "time":   current_time,
              })

    # commit change
    conn.commit()
    # close connection
    conn.close()


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
        add(final)
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

def history_window():
    app.withdraw()
    top = Toplevel()
    top.title("HISTORY")
    top.configure(background='black')

    variable = StringVar(top)
    quality_combo = ttk.Combobox(top, width=27, font="arial", textvariable=variable)

    my_label = Label(top, text="HISTORY", font="arial", fg="blue", bg="cyan")
    my_label.grid(row=0, column=0, padx=(10, 0), pady=(10, 20))


    def callbackFunc(event):  # this function used to get selected item from the combo box and load into oid i/p box
        """when the item choose from the combobox it load to choice"""
        choice = quality_combo.get()
        choice = int((choice.strip())[0])

        oid.delete(0,1)
        oid.insert(0, choice)


    def show_data():  # this function used to show data in combo box whenever show button hit
        quality_combo['values'] = ()

        quality_list = []

        conn = sqlite3.connect("weather_database.db")
        c = conn.cursor()

        # retrive all data from the student table and load all data into records
        c.execute("SELECT *, oid FROM weather_info")
        records = c.fetchall()

        conn.commit()
        conn.close()

        for record in records:
            quality_list.append(str(record[7]) + " " + str(record[0]) + "-" + str(record[4])+ "," +str(record[2]) + "\n "
                                +str(record[5]) + " " + str(record[6]))

        quality_combo['values'] = tuple(quality_list)
        quality_combo.grid(row=2, column=0, columnspan=2, pady=10, padx=10, ipadx=50)
        quality_combo.bind("<<ComboboxSelected>>", callbackFunc)  # call callback function when record selected

    # show and exit button
    show_btn = Button(top, text="SHOW DATA", font="arial", fg="red", bg="yellow", command=show_data)
    show_btn.grid(row=5, column=0, pady=10, padx=10, ipadx=22)

    oid = Entry(top, text="", font="arial", fg="white", bg="black")
    oid.grid(row=6, column=1, padx=(0,1),pady=10, ipadx=1)

    def delete(no):
        try:
            conn = sqlite3.connect("weather_database.db")
            c = conn.cursor()

            # delete a record
            c.execute(f"DELETE from weather_info WHERE oid= " + str(no))

            conn.commit()
            conn.close()

            messagebox.showinfo("Message", "DATA DELETE SUCCESSFULLY")

        except:
            messagebox.showerror("Message", "OPERATION UNSUCESSFUL \n PLEEASE TRY AGAIN")

    delete_btn = Button(top, text="DELETE DATA", font="arial", fg="black", bg="violet", command=lambda: delete(oid.get()))
    delete_btn.grid(row=6, column=0, pady=10, padx=10, ipadx=14)

    def hide_open2():
        app.deiconify()
        top.destroy()

    exit2_btn = Button(top, text="EXIT", font="arial", fg="yellow", bg="red", command=hide_open2)
    exit2_btn.grid(row=8, column=0,pady=10,ipadx=5)


history_btn = Button(app, text="History", font="arial", fg="yellow", bg="Green",padx=55, command=history_window)
history_btn.grid(row=8, column=1, padx=(0,50), pady=(10, 0))

exit_btn = Button(app, text="Exit", command=app.quit, font="arial", fg="white", bg="red",padx=70)
exit_btn.grid(row=9, column=1, padx=(0,50), pady=(10, 0))

app.mainloop()
