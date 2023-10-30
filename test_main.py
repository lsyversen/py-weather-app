import main  # Import the module containing your application code

def test_valid_city():
    city = "Detroit"
    result = main.get_weather(city)
    assert result is not None, f"Expected weather information for {city}, but got None."
    print("Test 1: Passed")

def test_invalid_city():
    city = "Random"
    result = main.get_weather(city)
    assert result is None, f"Expected None for an invalid city ({city}), but got weather information."
    print("Test 2: Passed")

def test_temperature_unit_toggle():
    initial_text = main.temperature_label.cget("text")

    # Toggle the temperature unit
    main.toggle_temperature_unit()
    new_text = main.temperature_label.cget("text")

    # If the initial text was in Celsius, it should now be in Fahrenheit, and vice versa.
    if "°C" in initial_text:
        assert "°F" in new_text, "Failed to toggle from Celsius to Fahrenheit."
    else:
        assert "°C" in new_text, "Failed to toggle from Fahrenheit to Celsius."
    
    print("Test 3: Passed")

if __name__ == "__main__":
    test_valid_city()
    test_invalid_city()
    test_temperature_unit_toggle()





