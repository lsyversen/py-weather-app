# Import required modules
import tkinter as tk
import requests
from tkinter import messagebox
from PIL import Image, ImageTk
import ttkbootstrap
import database  

# Function to get weather information from OpenWeatherMap API
def get_weather(city):
    API_key = "39fe395e3d3df0ea4631cf069be88415"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}"
    res = requests.get(url)

    if res.status_code == 404:
        messagebox.showerror("Error", "City not found")
        return None
    
    # Parse the response JSON to get weather information
    weather = res.json()
    icon_id = weather['weather'][0]['icon']
    temperature = weather['main']['temp'] - 273.15
    description = weather['weather'][0]['description']
    city = weather['name']
    country = weather['sys']['country']

    # Get the icon URL and return all the weather information
    icon_url = f"http://openweathermap.org/img/wn/{icon_id}@2x.png"
    return (icon_url, temperature, description, city, country)

# Function to update the GUI and database with user input and response
def update_weather_info():
    city = city_entry.get()
    result = get_weather(city)
    if result is None:
        return

    # If the city is found, unpack the weather information
    icon_url, temperature, description, city, country = result

    # Update the GUI with weather information
    location_label.configure(text=f"{city}, {country}")

    image = Image.open(requests.get(icon_url, stream=True).raw)
    icon = ImageTk.PhotoImage(image)
    icon_label.configure(image=icon)
    icon_label.image = icon

    temperature_label.configure(text=f"Temperature: {temperature:.2f}°C")
    description_label.configure(text=f"Description: {description}")

    # Insert user input and response into the database
    database.insert_response(city, f"Temperature: {temperature:.2f}°C, Description: {description}")

# Create the SQLite database and table
database.create_database()

root = ttkbootstrap.Window(themename="morph")
root.title("Weather App")
root.geometry("400x400")

# Function to open a new window to display weather history
def show_weather_history():
    # Create a new window
    history_window = tk.Toplevel()
    history_window.title("Weather History")

    # Retrieve all user responses from the database
    responses = database.get_all_responses()

    if not responses:
        tk.Label(history_window, text="No weather history available").pack(pady=20)
    else:
        # Create a listbox to display the history
        history_listbox = tk.Listbox(history_window, font="Helvetica, 14", selectmode=tk.SINGLE, width=40)
        history_listbox.pack(pady=20)

        # Add responses to the listbox
        for user_input, response_text in responses:
            history_listbox.insert(tk.END, f"User input: {user_input}, Response: {response_text}")

# Function to toggle between Celsius and Fahrenheit
def toggle_temperature_unit():
    current_text = temperature_label.cget("text")
    if "°C" in current_text:
        # If the current temperature is in Celsius, switch to Fahrenheit
        temperature_in_fahrenheit = (float(current_text.split(":")[1].replace("°C", "").strip()) * 9/5) + 32
        temperature_label.configure(text=f"Temperature: {temperature_in_fahrenheit:.2f}°F")
    else:
        # If the current temperature is in Fahrenheit, switch to Celsius
        temperature_in_celsius = (float(current_text.split(":")[1].replace("°F", "").strip()) - 32) * 5/9
        temperature_label.configure(text=f"Temperature: {temperature_in_celsius:.2f}°C")

# Create a button to toggle temperature unit
unit_button = ttkbootstrap.Button(root, text="Toggle Unit", command=toggle_temperature_unit, bootstyle="success")
unit_button.pack(pady=10)

# Create a button to open the weather history window
history_button = ttkbootstrap.Button(root, text="View Weather History", command=show_weather_history, bootstyle="info")
history_button.pack(pady=10)

# Create an entry widget to enter the city name
city_entry = ttkbootstrap.Entry(root, font="Helvetica, 18")
city_entry.pack(pady=10)

# Create a button widget to search for the weather information
search_button = ttkbootstrap.Button(root, text="Search", command=update_weather_info, bootstyle="warning")
search_button.pack(pady=10)

# Create a label widget to show the city/country name
location_label = tk.Label(root, font="Helvetica, 25")
location_label.pack(pady=20)

# Create a label widget to show the weather icon
icon_label = tk.Label(root)
icon_label.pack()

# Create a label widget -> to show the temperature
temperature_label = tk.Label(root, font="Helvetica, 20")
temperature_label.pack()

# Create a label widget -> to show the weather description
description_label = tk.Label(root, font="Helvetica, 20")
description_label.pack()

root.mainloop()

#tests
def test_valid_city():
    city = "Detroit"
    result = get_weather(city)
    assert result is not None, f"Expected weather information for {city}, but got None."
    print("Test 1: Passed")

test_valid_city()

