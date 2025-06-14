import requests
import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
from io import BytesIO

API_KEY = "45b01a7f6a9893cc9370a6fd91f105fb"  
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def fetch_weather():
    city = city_entry.get()
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name.")
        return
    
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    }

    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        weather = data['weather'][0]
        main = data['main']
        icon_code = weather['icon']

        result.set(f"Weather in {data['name']}:\n"
                   f"Condition: {weather['description'].capitalize()}\n"
                   f"Temperature: {main['temp']}°C\n"
                   f"Humidity: {main['humidity']}%")
        
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        icon_response = requests.get(icon_url)
        icon_img = Image.open(BytesIO(icon_response.content))
        icon_tk = ImageTk.PhotoImage(icon_img)
        icon_label.config(image=icon_tk)
        icon_label.image = icon_tk
    else:
        result.set("Error: Could not retrieve weather data.")

# GUI setup
root = tk.Tk()
root.title("Weather App")
root.geometry("350x400")

tk.Label(root, text="Enter City:", font=("Arial", 12)).pack(pady=10)
city_entry = tk.Entry(root, width=25, font=("Arial", 12))
city_entry.pack()

tk.Button(root, text="Get Weather", command=fetch_weather, font=("Arial", 12)).pack(pady=10)

icon_label = tk.Label(root)
icon_label.pack()

result = tk.StringVar()
tk.Label(root, textvariable=result, font=("Arial", 12), justify="center").pack(pady=20)

root.mainloop()
