import tkinter as tk
from tkinter import messagebox
import requests
from datetime import datetime, timedelta

# API Key
API_KEY = "93ce9b7baf1a84e19bafb43d890bc38b"  # Replace with your OpenWeatherMap API key

# Function to fetch latitude and longitude
def get_coordinates(city):
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&appid={API_KEY}"
    response = requests.get(geo_url)
    if response.status_code == 200:
        data = response.json()
        if data:
            return data[0]["lat"], data[0]["lon"]
        else:
            raise ValueError("City not found!")
    else:
        response.raise_for_status()

# Function to fetch current and next-day weather
def get_weather():
    city = city_entry.get().strip()
    if not city:
        messagebox.showerror("Error", "Please enter a city name!")
        return
    
    # Show loading message
    result_label.config(text="Fetching weather data...")
    
    try:
        # Get coordinates
        lat, lon = get_coordinates(city)
        
        # Fetch weather data
        weather_url = f"http://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly,alerts&units=metric&appid={API_KEY}"
        response = requests.get(weather_url)
        data = response.json()
        
        if response.status_code != 200:
            result_label.config(text="")
            messagebox.showerror("Error", data.get("message", "Unable to fetch data"))
            return
        
        # Current weather
        current = data["current"]
        temp = current["temp"]
        weather = current["weather"][0]["description"]
        humidity = current["humidity"]
        
        # Next day's weather
        next_day = data["daily"][1]
        next_temp_day = next_day["temp"]["day"]
        next_temp_night = next_day["temp"]["night"]
        next_weather = next_day["weather"][0]["description"]
        
        # Format sunrise and sunset times
        sunrise = datetime.fromtimestamp(current["sunrise"]).strftime('%H:%M:%S')
        sunset = datetime.fromtimestamp(current["sunset"]).strftime('%H:%M:%S')
        
        # Update result label
        result_label.config(
            text=f"City: {city.capitalize()}\n"
                 f"Current Temperature: {temp}°C\n"
                 f"Weather: {weather.capitalize()}\n"
                 f"Humidity: {humidity}%\n"
                 f"Sunrise: {sunrise}\n"
                 f"Sunset: {sunset}\n\n"
                 f"--- Next Day Forecast ---\n"
                 f"Day Temperature: {next_temp_day}°C\n"
                 f"Night Temperature: {next_temp_night}°C\n"
                 f"Weather: {next_weather.capitalize()}"
        )
        
    except Exception as e:
        result_label.config(text="")
        messagebox.showerror("Error", f"Unable to fetch data: {e}")

# Tkinter GUI
app = tk.Tk()
app.title("Weather App")

# Entry for City Name with Placeholder Text
city_label = tk.Label(app, text="Enter City:", font=("Arial", 14))
city_label.pack(pady=10)

city_entry = tk.Entry(app, width=30, font=("Arial", 14))
city_entry.pack(pady=10)
city_entry.insert(0, "Type a city name...")

def clear_placeholder(event):
    if city_entry.get() == "Type a city name...":
        city_entry.delete(0, tk.END)

city_entry.bind("<FocusIn>", clear_placeholder)

# Fetch Button
fetch_button = tk.Button(app, text="Get Weather", command=get_weather, font=("Arial", 14))
fetch_button.pack(pady=10)

# Result Display
result_label = tk.Label(app, text="", font=("Arial", 14), justify="left", wraplength=400)
result_label.pack(pady=20)

# Run the app
app.geometry("500x500")
app.mainloop()
