import requests
import logging
import re

# Configurazione logging opzionale
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_weather_data(city, timeout=10):
    """
    Recupera i dati meteorologici per una città specifica utilizzando l'API Open-Meteo.

    Args:
        city (str): Nome della città da cercare
        timeout (int): Timeout in secondi per le richieste HTTP (default: 10)

    Returns:
        dict: Dizionario contenente:
            - Se successo: {'city', 'temperature', 'condition', 'humidity', 'wind_speed'}
            - Se errore: {'error': 'messaggio di errore descrittivo'}

    Raises:
        ValueError: Se il parametro city è invalido
        requests.RequestException: Per errori di connessione
    """
    # Validazione parametri di input
    if not isinstance(city, str) or not city.strip():
        logger.warning("Parametro città invalido: %s", city)
        return {'error': 'Nome città non valido. Inserisci una stringa non vuota.'}

    city = city.strip()

    # Validazione aggiuntiva: rifiuta input che sembrano coordinate o numeri
    # Controlla se è composto solo da numeri e caratteri di punteggiatura (coordinate)
    if re.match(r'^[\d\s,.-]+$', city):
        logger.warning("Input sembra essere una coordinata o numero: %s", city)
        return {'error': 'Input non valido. Inserisci il nome di una città, non coordinate o numeri.'}

    # Controlla se non contiene almeno una lettera (nomi di città dovrebbero avere lettere)
    if not re.search(r'[a-zA-Z]', city):
        logger.warning("Input non contiene lettere: %s", city)
        return {'error': 'Nome città non valido. Inserisci il nome di una città con lettere.'}

    try:
        # Fase 1: Geocoding - ottieni coordinate dalla città
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"

        logger.info("Richiesta geocoding per città: %s", city)
        geo_response = requests.get(geo_url, timeout=timeout)

        # Verifica status code
        geo_response.raise_for_status()

        # Parsing JSON sicuro
        geo_data = geo_response.json()

        # Verifica presenza risultati
        if not geo_data.get('results'):
            logger.warning("Nessun risultato geocoding per città: %s", city)
            return {'error': f'Città "{city}" non trovata. Verifica il nome e riprova.'}

        # Estrai coordinate
        location = geo_data['results'][0]
        lat = location['latitude']
        lon = location['longitude']

        logger.info("Coordinate trovate: lat=%s, lon=%s", lat, lon)

        # Fase 2: Recupero dati meteo
        weather_url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}&"
            f"current_weather=true&"
            f"hourly=temperature_2m,relative_humidity_2m,windspeed_10m&"
            f"timezone=auto"
        )

        logger.info("Richiesta dati meteo per coordinate: %s, %s", lat, lon)
        weather_response = requests.get(weather_url, timeout=timeout)
        weather_response.raise_for_status()

        # Parsing dati meteo
        weather_data = weather_response.json()

        # Estrai dati attuali
        current_weather = weather_data.get('current_weather', {})
        hourly_data = weather_data.get('hourly', {})

        if not current_weather:
            logger.error("Dati current_weather mancanti nella risposta")
            return {'error': 'Dati meteo temporaneamente non disponibili. Riprova più tardi.'}

        # Estrai valori con fallback sicuri
        temperature = current_weather.get('temperature')
        weathercode = current_weather.get('weathercode', 0)
        wind_speed = current_weather.get('windspeed')

        # Umidità dal primo valore orario
        humidity_list = hourly_data.get('relative_humidity_2m', [])
        humidity = humidity_list[0] if humidity_list else None

        # Determina condizione atmosferica (mappatura migliorata)
        condition = _map_weather_code_to_condition(weathercode)

        # Validazione dati essenziali
        if temperature is None or wind_speed is None:
            logger.error("Dati essenziali mancanti: temperature=%s, wind_speed=%s", temperature, wind_speed)
            return {'error': 'Dati meteo incompleti ricevuti dall\'API. Riprova più tardi.'}

        result = {
            'city': city,
            'temperature': temperature,
            'condition': condition,
            'humidity': humidity,
            'wind_speed': wind_speed
        }

        logger.info("Dati meteo recuperati con successo per %s", city)
        return result

    except requests.exceptions.Timeout:
        logger.error("Timeout nella richiesta per città: %s", city)
        return {'error': f'Timeout nella connessione per "{city}". Controlla la connessione internet e riprova.'}
    except requests.exceptions.ConnectionError:
        logger.error("Errore di connessione per città: %s", city)
        return {'error': f'Errore di connessione per "{city}". Verifica la connessione internet.'}
    except requests.exceptions.HTTPError as e:
        status_code = getattr(e.response, 'status_code', 'Unknown') if e.response else 'Unknown'
        logger.error("Errore HTTP %s per città: %s", status_code, city)
        return {'error': f'Servizio meteo temporaneamente non disponibile (Errore {status_code}). Riprova più tardi.'}
    except ValueError as e:
        logger.error("Errore parsing JSON per città: %s - %s", city, str(e))
        return {'error': 'Risposta del server malformata. Riprova più tardi.'}
    except KeyError as e:
        logger.error("Chiave mancante nella risposta API per città: %s - %s", city, str(e))
        return {'error': 'Dati meteo non disponibili nel formato atteso. Riprova più tardi.'}
    except Exception as e:
        logger.error("Errore inatteso per città: %s - %s", city, str(e))
        return {'error': f'Errore inatteso durante il recupero dati per "{city}". Riprova più tardi.'}


def _map_weather_code_to_condition(weathercode):
    """
    Mappa il codice meteo Open-Meteo a una descrizione leggibile.

    Args:
        weathercode (int): Codice meteo da Open-Meteo

    Returns:
        str: Descrizione delle condizioni atmosferiche
    """
    # Mappatura basata sulla documentazione Open-Meteo
    weather_map = {
        0: "Sunny",
        1: "Mainly Sunny",
        2: "Partly Cloudy",
        3: "Cloudy",
        45: "Foggy",
        48: "Foggy",
        51: "Light Drizzle",
        53: "Drizzle",
        55: "Heavy Drizzle",
        56: "Light Freezing Drizzle",
        57: "Freezing Drizzle",
        61: "Light Rain",
        63: "Rain",
        65: "Heavy Rain",
        66: "Light Freezing Rain",
        67: "Freezing Rain",
        71: "Light Snow",
        73: "Snow",
        75: "Heavy Snow",
        77: "Snow Grains",
        80: "Light Rain Showers",
        81: "Rain Showers",
        82: "Heavy Rain Showers",
        85: "Light Snow Showers",
        86: "Snow Showers",
        95: "Thunderstorm",
        96: "Thunderstorm with Hail",
        99: "Heavy Thunderstorm with Hail"
    }

    return weather_map.get(weathercode, "Unknown")