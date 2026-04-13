from models import WeatherData

def display_weather(weather_data):
    if not weather_data:
        print("Errore: Impossibile recuperare i dati meteo.")
        return
    
    print(f"🌤️ Meteo per        {weather_data.city}:")
    print(f"   Temperatura:    {weather_data.temperature}°C")
    print(f"   Condizioni:     {weather_data.condition}")
    print(f"   Umidità:        {weather_data.humidity}%")
    print(f"   Velocità vento: {weather_data.wind_speed} km/h")
    print("\n")