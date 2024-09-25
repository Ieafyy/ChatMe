import requests

def get_current_temperature(city, api_key):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': '7612039fdd4e6f05c24099e2829519ef',
        'units': 'metric'  # Use 'imperial' for Fahrenheit
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        temperature = data['main']['temp']
        return temperature
    else:
        print("Error:", response.status_code, response.json().get('message', ''))
        return None

# Example usage
if __name__ == "__main__":
    api_key = "YOUR_API_KEY"  # Replace with your OpenWeatherMap API key
    city = "Contagem"
    temp = get_current_temperature(city, api_key)
    if temp is not None:
        print(f"The current temperature in {city} is {temp}°C")

