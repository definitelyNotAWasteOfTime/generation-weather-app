import unittest
from unittest.mock import patch, MagicMock
import requests
import logging
from src.weather_api import get_weather_data, _map_weather_code_to_condition

class TestWeatherAPI(unittest.TestCase):
    def test_get_weather_data_valid_city(self):
        data = get_weather_data("Rome")
        self.assertIsNotNone(data)
        self.assertIn('temperature', data)
    
    def test_get_weather_data_invalid_city(self):
        data = get_weather_data("InvalidCity123")
        self.assertIn('error', data)
        self.assertIn('non trovata', data['error'])
    
    # ===== Errori lato CLIENT =====
    def test_get_weather_data_empty_city(self):
        """Test con parametro città vuoto"""
        data = get_weather_data("")
        self.assertIn('error', data)
        self.assertIn('non valido', data['error'])
    
    @patch('src.weather_api.requests.get')
    def test_get_weather_data_connection_timeout(self, mock_get):
        """Test timeout di connessione (errore lato client)"""
        mock_get.side_effect = requests.exceptions.Timeout("Connection timeout")
        
        # Ora la funzione cattura l'eccezione e ritorna dict con errore
        data = get_weather_data("Rome")
        self.assertIn('error', data)
        self.assertIn('Timeout', data['error'])
    
    @patch('src.weather_api.requests.get')
    def test_get_weather_data_connection_error(self, mock_get):
        """Test errore di connessione (errore lato client)"""
        mock_get.side_effect = requests.exceptions.ConnectionError("Connection failed")
        
        # Ora la funzione cattura l'eccezione e ritorna dict con errore
        data = get_weather_data("Rome")
        self.assertIn('error', data)
        self.assertIn('connessione', data['error'])
    
    # ===== Errori lato SERVER =====
    @patch('src.weather_api.requests.get')
    def test_get_weather_data_geocoding_server_error(self, mock_get):
        """Test errore 500 dall'API di geocoding (errore lato server)"""
        mock_get.side_effect = requests.exceptions.HTTPError("500 Server Error")
        
        data = get_weather_data("Rome")
        self.assertIn('error', data)
        self.assertIn('non disponibile', data['error'])
    
    @patch('src.weather_api.requests.get')
    def test_get_weather_data_weather_server_error(self, mock_get):
        """Test errore 500 dall'API meteo (errore lato server)"""
        # Primo mock: geocoding ok
        geo_response = MagicMock()
        geo_response.status_code = 200
        geo_response.json.return_value = {
            'results': [{
                'latitude': 41.9028,
                'longitude': 12.4964
            }]
        }
        
        # Secondo mock: meteo error 500
        mock_get.side_effect = [geo_response, requests.exceptions.HTTPError("500 Server Error")]
        
        data = get_weather_data("Rome")
        self.assertIn('error', data)
        self.assertIn('non disponibile', data['error'])
    
    @patch('src.weather_api.requests.get')
    def test_get_weather_data_service_unavailable(self, mock_get):
        """Test errore 503 Service Unavailable (errore lato server)"""
        mock_get.side_effect = requests.exceptions.HTTPError("503 Service Unavailable")
        
        data = get_weather_data("Rome")
        self.assertIn('error', data)
        self.assertIn('non disponibile', data['error'])
    
    @patch('src.weather_api.requests.get')
    def test_get_weather_data_malformed_response(self, mock_get):
        """Test risposta malformata dall'API geocoding (errore lato server)"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}  # Risposta senza 'results'
        mock_get.return_value = mock_response
        
        data = get_weather_data("Rome")
        self.assertIn('error', data)
        self.assertIn('non trovata', data['error'])
    
    # ===== NUOVI TEST PER MIGLIORAMENTI RECENTI =====
    
    def test_get_weather_data_none_input(self):
        """Test input None (miglioramento validazione)"""
        data = get_weather_data(None)
        self.assertIn('error', data)
        self.assertIn('non valido', data['error'])
    
    def test_get_weather_data_int_input(self):
        """Test input intero (miglioramento validazione)"""
        data = get_weather_data(123)
        self.assertIn('error', data)
        self.assertIn('non valido', data['error'])
    
    def test_get_weather_data_list_input(self):
        """Test input lista (miglioramento validazione)"""
        data = get_weather_data([])
        self.assertIn('error', data)
        self.assertIn('non valido', data['error'])
    
    def test_get_weather_data_numeric_string_input(self):
        """Test input stringa numerica (coordinate o numeri)"""
        data = get_weather_data("12345")
        self.assertIn('error', data)
        self.assertIn('coordinate o numeri', data['error'])
    
    def test_get_weather_data_coordinates_input(self):
        """Test input coordinate geografiche"""
        data = get_weather_data("40.7128,-74.0060")
        self.assertIn('error', data)
        self.assertIn('coordinate o numeri', data['error'])
    
    def test_get_weather_data_no_letters_input(self):
        """Test input senza lettere (solo caratteri speciali)"""
        data = get_weather_data("!!!@@@###")
        self.assertIn('error', data)
        self.assertIn('con lettere', data['error'])
    
    def test_get_weather_data_whitespace_only(self):
        """Test input solo spazi bianchi (miglioramento pulizia input)"""
        data = get_weather_data("   ")
        self.assertIn('error', data)
        self.assertIn('non valido', data['error'])
    
    def test_get_weather_data_stripped_input(self):
        """Test che l'input venga pulito correttamente"""
        with patch('src.weather_api.requests.get') as mock_get:
            # Mock geocoding response
            geo_response = MagicMock()
            geo_response.status_code = 200
            geo_response.json.return_value = {
                'results': [{'latitude': 41.9028, 'longitude': 12.4964}]
            }
            
            # Mock weather response
            weather_response = MagicMock()
            weather_response.status_code = 200
            weather_response.json.return_value = {
                'current_weather': {'temperature': 22.5, 'windspeed': 8.3, 'weathercode': 0},
                'hourly': {'relative_humidity_2m': [65]}
            }
            
            mock_get.side_effect = [geo_response, weather_response]
            
            # Chiama con spazi extra
            data = get_weather_data("  Rome  ")
            
            # Verifica che la prima richiesta (geocoding) sia stata fatta con "Rome" pulito
            first_call_args, first_call_kwargs = mock_get.call_args_list[0]
            self.assertIn('name=Rome', first_call_args[0])
            
            # Verifica che il risultato contenga la città pulita
            self.assertIsNotNone(data)
            self.assertEqual(data['city'], 'Rome')
    
    @patch('src.weather_api.requests.get')
    def test_get_weather_data_custom_timeout(self, mock_get):
        """Test timeout personalizzato"""
        mock_get.side_effect = requests.exceptions.Timeout("Connection timeout")
        
        # Test con timeout personalizzato
        data = get_weather_data("Rome", timeout=5)
        self.assertIn('error', data)
        self.assertIn('Timeout', data['error'])
        
        # Verifica che il timeout sia stato passato correttamente
        args, kwargs = mock_get.call_args
        self.assertEqual(kwargs['timeout'], 5)
    
    @patch('src.weather_api.requests.get')
    def test_get_weather_data_value_error_json(self, mock_get):
        """Test ValueError durante parsing JSON"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_get.return_value = mock_response
        
        data = get_weather_data("Rome")
        self.assertIn('error', data)
        self.assertIn('malformata', data['error'])
    
    @patch('src.weather_api.requests.get')
    def test_get_weather_data_key_error_response(self, mock_get):
        """Test KeyError quando manca una chiave essenziale nella risposta"""
        # Mock geocoding ok
        geo_response = MagicMock()
        geo_response.status_code = 200
        geo_response.json.return_value = {
            'results': [{'latitude': 41.9028, 'longitude': 12.4964}]
        }
        
        # Mock weather response senza 'current_weather'
        weather_response = MagicMock()
        weather_response.status_code = 200
        weather_response.json.return_value = {'hourly': {}}
        
        mock_get.side_effect = [geo_response, weather_response]
        
        data = get_weather_data("Rome")
        self.assertIn('error', data)
        self.assertIn('non disponibili', data['error'])
    
    @patch('src.weather_api.requests.get')
    def test_get_weather_data_missing_essential_data(self, mock_get):
        """Test quando dati essenziali (temperature/wind_speed) sono None"""
        # Mock geocoding ok
        geo_response = MagicMock()
        geo_response.status_code = 200
        geo_response.json.return_value = {
            'results': [{'latitude': 41.9028, 'longitude': 12.4964}]
        }
        
        # Mock weather response con dati essenziali mancanti
        weather_response = MagicMock()
        weather_response.status_code = 200
        weather_response.json.return_value = {
            'current_weather': {'weathercode': 0},  # Mancano temperature e windspeed
            'hourly': {'relative_humidity_2m': [65]}
        }
        
        mock_get.side_effect = [geo_response, weather_response]
        
        data = get_weather_data("Rome")
        self.assertIn('error', data)
        self.assertIn('incompleti', data['error'])
    
    def test_map_weather_code_to_condition_known_codes(self):
        """Test mappatura weathercode conosciuti"""
        test_cases = [
            (0, "Sunny"),
            (1, "Mainly Sunny"),
            (2, "Partly Cloudy"),
            (3, "Cloudy"),
            (45, "Foggy"),
            (61, "Light Rain"),
            (63, "Rain"),
            (71, "Light Snow"),
            (73, "Snow"),
            (95, "Thunderstorm"),
            (99, "Heavy Thunderstorm with Hail")
        ]
        
        for code, expected in test_cases:
            with self.subTest(code=code):
                result = _map_weather_code_to_condition(code)
                self.assertEqual(result, expected)
    
    def test_map_weather_code_to_condition_unknown_code(self):
        """Test mappatura weathercode sconosciuto"""
        result = _map_weather_code_to_condition(999)
        self.assertEqual(result, "Unknown")
    
    def test_map_weather_code_to_condition_negative_code(self):
        """Test mappatura weathercode negativo"""
        result = _map_weather_code_to_condition(-1)
        self.assertEqual(result, "Unknown")
    
    @patch('src.weather_api.logger')
    def test_logging_on_invalid_input(self, mock_logger):
        """Test che il logging funzioni per input invalido"""
        data = get_weather_data("")
        mock_logger.warning.assert_called_with("Parametro città invalido: %s", "")
        self.assertIn('error', data)
    
    @patch('src.weather_api.requests.get')
    @patch('src.weather_api.logger')
    def test_logging_on_success(self, mock_logger, mock_get):
        """Test logging di successo"""
        # Setup mock per successo
        geo_response = MagicMock()
        geo_response.status_code = 200
        geo_response.json.return_value = {
            'results': [{'latitude': 41.9028, 'longitude': 12.4964}]
        }
        
        weather_response = MagicMock()
        weather_response.status_code = 200
        weather_response.json.return_value = {
            'current_weather': {'temperature': 22.5, 'windspeed': 8.3, 'weathercode': 0},
            'hourly': {'relative_humidity_2m': [65]}
        }
        
        mock_get.side_effect = [geo_response, weather_response]
        
        data = get_weather_data("Rome")
        
        # Verifica logging di successo
        mock_logger.info.assert_any_call("Dati meteo recuperati con successo per %s", "Rome")
        self.assertNotIn('error', data)
    
    @patch('src.weather_api.requests.get')
    @patch('src.weather_api.logger')
    def test_logging_on_timeout(self, mock_logger, mock_get):
        """Test logging di timeout"""
        mock_get.side_effect = requests.exceptions.Timeout("Timeout")
        
        data = get_weather_data("Rome")
        
        mock_logger.error.assert_called_with("Timeout nella richiesta per città: %s", "Rome")
        self.assertIn('error', data)
    
    @patch('src.weather_api.requests.get')
    @patch('src.weather_api.logger')
    def test_logging_on_connection_error(self, mock_logger, mock_get):
        """Test logging di errore connessione"""
        mock_get.side_effect = requests.exceptions.ConnectionError("Connection failed")
        
        data = get_weather_data("Rome")
        
        mock_logger.error.assert_called_with("Errore di connessione per città: %s", "Rome")
        self.assertIn('error', data)
    
    @patch('src.weather_api.requests.get')
    @patch('src.weather_api.logger')
    def test_logging_on_http_error(self, mock_logger, mock_get):
        """Test logging di errore HTTP"""
        mock_get.side_effect = requests.exceptions.HTTPError("500 Server Error")
        
        data = get_weather_data("Rome")
        
        mock_logger.error.assert_called_with("Errore HTTP %s per città: %s", "Unknown", "Rome")
        self.assertIn('error', data)