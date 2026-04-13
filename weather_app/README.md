# 🌤️ Weather App

Una semplice applicazione meteo in Python che recupera dati meteorologici da **Open-Meteo** in tempo reale. L'app consente agli utenti di visualizzare temperatura, condizioni atmosferiche, umidità e velocità del vento per qualsiasi città nel mondo attraverso un'**interfaccia grafica molto semplice, responsive e user-friendly**.

---

## 📋 Indice
- [Panoramica](#-panoramica-del-progetto)
- [Installazione](#-installazione)
- [Utilizzo](#-guida-allutilizzo)
- [Esempio di Output](#-output-di-esempio)
- [Funzionalità](#-funzionalità)
- [Gestione degli Errori](#-gestione-degli-errori)
- [API Utilizzate](#-api-utilizzate)
- [Miglioramenti Implementati](#-miglioramenti-implementati)
- [Miglioramenti Futuri](#-miglioramenti-futuri)
- [Testing](#-testing)

---

## 🎯 Panoramica del Progetto

**Weather App** è un'applicazione concepita per fornire informazioni meteorologiche accurate e aggiornate. L'app:

- ✅ Ricerca automatica della città usando **geocoding**
- ✅ Recupera dati meteo in tempo reale da **Open-Meteo**
- ✅ Visualizza temperatura, condizioni, umidità e velocità del vento
- ✅ Gestisce errori di connessione e input non validi
- ✅ **Validazione input avanzata** - rifiuta numeri e coordinate
- ✅ **Interfaccia grafica responsive** - finestra ridimensionabile con layout adattivo
- ✅ Supporta qualsiasi città nel mondo
- ✅ **Logging avanzato** per monitoraggio e debugging
- ✅ **Gestione errori robusta** con timeout configurabili
- ✅ **25+ condizioni atmosferiche** dettagliate

---

## 💻 Installazione

### Prerequisiti
- Python 3.8 o superiore
- pip (gestore pacchetti Python)

### Passaggi

1. **Clona o scarica il progetto:**
   ```bash
   git clone https://github.com/definitelyNotAWasteOfTime/generation-weather-app.git
   cd weather-app
   ```

2. **Installa le dipendenze:**
   ```bash
   pip install -r requirements.txt
   ```

   Le dipendenze richieste sono:
   - `requests`: per effettuare richieste HTTP alle API
   - `pytest`: per eseguire i test (facoltativo)

3. **Verifica l'installazione:**
   ```bash
   python src/main.py
   ```
   
   *Alternativa: `python -m src.main` (se si preferisce l'esecuzione come modulo)*

---

## 🚀 Guida all'Utilizzo

### Esecuzione Base

1. Avvia l'applicazione:
   ```bash
   python src/main.py
   ```
   
   *Oppure come modulo:*
   ```bash
   python -m src.main
   ```

2. Si aprirà una finestra grafica responsive con un'interfaccia intuitiva:
   - Inserisci il nome della città nel campo di testo
   - Premi "Ottieni Meteo" o invio per recuperare i dati
   - I risultati verranno visualizzati nell'area scrollabile
   - La finestra può essere ridimensionata per adattarsi alle tue esigenze

### Funzionamento Interno

L'applicazione segue questo flusso:

1. **Input utente**: Acquisisce il nome della città tramite interfaccia grafica
2. **Geocoding**: Converte il nome della città in coordinate (latitudine/longitudine)
3. **Recupero dati**: Ottiene i dati meteo attuali tramite Open-Meteo
4. **Visualizzazione**: Formatta e mostra i risultati nell'interfaccia grafica

---

## 📊 Output di Esempio

### Interfaccia Grafica

L'applicazione presenta una finestra grafica intuitiva con:

- **Campo di input**: Per inserire il nome della città
- **Pulsante "Ottieni Meteo"**: Per avviare la ricerca
- **Area risultati**: Visualizza i dati meteo formattati
- **Area errori**: Mostra messaggi di errore in rosso

### Esempio di Risultato (Design Moderno)

Dopo aver inserito "Roma" e premuto "OTTieni Meteo":

```
📍 LOCALITÀ: ROME
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TEMPERATURA:  21.8°C 🌡️
CONDIZIONI:   Cloudy 🌤️
UMIDITÀ:      84% 💧
VENTO:        2.3 km/h 💨

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 Dati aggiornati in tempo reale da Open-Meteo
```

### Esempio con Errore

Se inserisci una città non valida come "InvalidCity123":

```
❌ Città "InvalidCity123" non trovata. Verifica il nome e riprova.
```

```
Inserisci il nome di una città: 
Città non valida.
```

---

## ⚡ Funzionalità

| Funzionalità | Descrizione |
|---|---|
| 🌍 **Geocoding Automatico** | Converte nomi di città in coordinate geografiche |
| 🌡️ **Temperatura Attuale** | Mostra la temperatura in °C |
| 💨 **Velocità del Vento** | Visualizza la velocità del vento in km/h |
| 💧 **Umidità Relativa** | Indica il livello di umidità in percentuale |
| 🌦️ **Condizioni Atmosferiche** | Fornisce lo stato atmosferico dettagliato (25+ condizioni) |
| 🔍 **Validazione Input** | Controlla validità e tipo dei dati inseriti |
| 📱 **Interfaccia Intuitiva** | Design semplice e facile da usare |
| ⏱️ **Timeout Configurabile** | Timeout 10 secondi per richieste API |
| 📝 **Logging Avanzato** | Logging dettagliato per debugging e monitoraggio |
| 🛡️ **Gestione Errori Robusta** | Cattura e gestisce tutte le eccezioni possibili |

---

## 🛡️ Gestione degli Errori

L'applicazione gestisce diversi tipi di errori con logging dettagliato:

### Errori Lato Client

| Errore | Gestione |
|---|---|
| **Input invalido** | Type checking e validazione contenuto |
| **Input vuoto/spazi** | Pulizia automatica con `.strip()` |
| **Timeout connessione** | Timeout 10 secondi configurabile |
| **Errore di connessione** | Cattura `ConnectionError` con logging |
| **Errore di rete** | Gestione `RequestException` generica |

### Errori Lato Server

| Errore | Gestione |
|---|---|
| **Città non trovata** | Controllo presenza risultati geocoding |
| **Errore HTTP (4xx/5xx)** | Cattura `HTTPError` con status code |
| **Risposta malformata** | Validazione struttura JSON |
| **Chiavi mancanti** | Fallback sicuri con `.get()` |
| **Dati essenziali nulli** | Validazione prima del ritorno |

### Errori di Parsing

| Errore | Gestione |
|---|---|
| **JSON invalido** | Cattura `ValueError` in parsing |
| **Chiavi mancanti** | Cattura `KeyError` con fallback |
| **Weathercode sconosciuto** | Mappatura a "Unknown" |

### Messaggi di Errore Specifici

L'applicazione ora fornisce **messaggi di errore dettagliati e user-friendly**:

- ❌ **Input invalido**: "Nome città non valido. Inserisci una stringa non vuota."
- ❌ **Input numerico/coordinate**: "Input non valido. Inserisci il nome di una città, non coordinate o numeri."
- ❌ **Input senza lettere**: "Nome città non valido. Inserisci il nome di una città con lettere."
- ❌ **Città non trovata**: 'Città "InvalidCity" non trovata. Verifica il nome e riprova.'
- ❌ **Timeout**: 'Timeout nella connessione per "Rome". Controlla la connessione internet e riprova.'
- ❌ **Errore connessione**: 'Errore di connessione per "Rome". Verifica la connessione internet.'
- ❌ **Servizio non disponibile**: 'Servizio meteo temporaneamente non disponibile (Errore 503). Riprova più tardi.'
- ❌ **Dati incompleti**: 'Dati meteo incompleti ricevuti dall\'API. Riprova più tardi.'

### Suite di Test

Una suite completa di **29 test** copre:
- ✅ Valori validi e città reali
- ✅ Errori client: timeout, connessione, input invalido
- ✅ Errori server: 500, 503, risposte malformate
- ✅ Parsing errori: JSON invalido, chiavi mancanti
- ✅ Validazione input: tipi, contenuto, numeri, coordinate
- ✅ **Nuovi test per miglioramenti:**
  - Input non-stringa (None, int, list)
  - Input numerico e coordinate geografiche
  - Input senza lettere (caratteri speciali)
  - Pulizia input e stripping
  - Timeout personalizzato
  - Mappatura weathercode completa
  - Logging e monitoraggio
  - Dati essenziali mancanti
  - Gestione eccezioni specifiche

Esegui i test con:
```bash
pytest tests/ -v
```

---

## 🔌 API Utilizzate

### 1. **Geocoding API - Open-Meteo**

Converte il nome della città in coordinate geografiche.

**Endpoint:**
```
https://geocoding-api.open-meteo.com/v1/search
```

**Parametri:**
- `name`: Nome della città
- `count`: Numero di risultati (default: 1)
- `language`: Lingua dei risultati
- `format`: Formato risposta (JSON)

**Risposta di Esempio:**
```json
{
  "results": [
    {
      "name": "Roma",
      "latitude": 41.9028,
      "longitude": 12.4964,
      "country": "Italy"
    }
  ]
}
```

### 2. **Weather Forecast API - Open-Meteo**

Recupera i dati meteorologici attuali.

**Endpoint:**
```
https://api.open-meteo.com/v1/forecast
```

**Parametri:**
- `latitude`: Latitudine della città
- `longitude`: Longitudine della città
- `current_weather`: Include dati meteo attuali
- `hourly`: Dati orari (temperature, umidità, velocità vento)
- `timezone`: Fuso orario automatico

**Risposta di Esempio:**
```json
{
  "current_weather": {
    "temperature": 22.5,
    "windspeed": 8.3,
    "weathercode": 0
  },
  "hourly": {
    "relative_humidity_2m": [65, 68, 70, ...]
  }
}
```

### Caratteristiche API Open-Meteo

✅ **Gratuita** - Nessuna chiave API necessaria  
✅ **Affidabile** - 99.9% uptime garantito  
✅ **Globale** - Copre tutto il mondo  
✅ **Veloce** - Risposta in millisecondi  

---

## ✅ Miglioramenti Implementati

### v2.1.0 - Applicazione Completa con GUI Responsive

**Weather App è ora un'applicazione completa con interfaccia grafica moderna e robusta backend API.**

### Interfaccia Grafica Moderna (Fase 1 Implementata)

L'applicazione presenta ora una **interfaccia grafica moderna e professionale** con design ispirato ai servizi meteorologici ufficiali:

- **🎨 Design Aeronautico**: Palette colori blu istituzionale (#003366) con sfondo chiaro
- **📱 Layout Card-Based**: Elementi organizzati in card bianche con bordi sottili
- **🔤 Font Moderni**: Utilizzo di Helvetica per un aspetto professionale
- **⚡ Interattività Migliorata**: Pulsanti con effetto hover e cursore hand
- **📊 Presentazione Dati**: Formattazione strutturata con separatori e icone
- **🔍 Campo Input Stilizzato**: Entry field con sfondo chiaro e bordi flat
- **📈 Header Risultati**: Sezione dedicata con header blu aeronautica
- **💻 Responsive Design**: Finestra ridimensionabile con layout adattivo

#### 🔧 **Backend API Robustezza e Logging Avanzato**
- ✅ **Docstring completa** con parametri, ritorni ed eccezioni
- ✅ **Commenti migliorati** e struttura logica del codice
- ✅ **Timeout configurabile** (10 secondi default) per evitare blocchi infiniti
- ✅ **Validazione input robusta** con type checking e regex avanzata
- ✅ **Pulizia automatica** input con `.strip()`
- ✅ **Logging dettagliato** con livelli appropriati per debugging

#### 🛡️ **Gestione Errori Avanzata**
- ✅ **Cattura eccezioni specifiche**: `Timeout`, `ConnectionError`, `HTTPError`, `ValueError`, `KeyError`
- ✅ **Validazione dati essenziali** prima del ritorno risultati
- ✅ **Fallback sicuri** per valori mancanti nelle risposte API
- ✅ **Messaggi di errore user-friendly** con contesto specifico
- ✅ **Rifiuto input numerici/coordinate** per prevenire interpretazioni errate

#### 🌦️ **Sistema Meteo Completo**
- ✅ **Mappatura completa** weathercode (0-99) invece di logica semplificata
- ✅ **25+ condizioni atmosferiche** dettagliate (Sunny, Rain, Snow, Thunderstorm, etc.)
- ✅ **Geocoding automatico** da nomi città a coordinate
- ✅ **API Open-Meteo** gratuite e affidabili
- ✅ **Gestione weathercode sconosciuti** con fallback a "Unknown"

#### 🧪 **Testing Completo**
- ✅ **Suite test estesa** da 9 a 29 test (+20 nuovi)
- ✅ **Mock corretti** per simulare eccezioni reali
- ✅ **Copertura completa**: validazione input, errori API, logging, timeout
- ✅ **Test per coordinate e numeri** rifiutati correttamente
- ✅ **Test per interfaccia** e funzionalità GUI

#### 📱 **Esperienza Utente Ottimale**
- ✅ **Navigazione intuitiva** - Layout logico e spaziatura chiara
- ✅ **Feedback visivo immediato** - Risultati e errori mostrati chiaramente
- ✅ **Interattività fluida** - Risposta rapida alle azioni utente
- ✅ **Pulizia automatica** - Campo input svuotato dopo ricerca riuscita
- ✅ **Supporto tastiera** - Invio possibile con tasto Enter

---

---

## 🚧 Miglioramenti Futuri

### Fase 2: Sfondo Dinamico
- **Sfondo che cambia in base alle condizioni meteo:**
  - ☀️ Sole: Sfondo giallo/arancione
  - ☁️ Nuvoloso: Sfondo grigio
  - 🌧️ Pioggia: Sfondo blu scuro
  - ❄️ Neve: Sfondo bianco/azzurro
  
- Animazioni fluide per transizioni tra stati

## 🧪 Testing

### Struttura dei Test

Il progetto include una suite di test completa in `tests/test_weather_api.py` che copre:

- **Test di validità**: Input validi e città reali
- **Errori client**: Timeout, errori di connessione, input vuoto
- **Errori server**: Status code 500, 503, risposte malformate

### Esecuzione dei Test

```bash
# Esegui tutti i test con pytest
pytest tests/ -v

# Esegui con unittest
python -m unittest discover -s tests -v

# Esegui un singolo test
pytest tests/test_weather_api.py::TestWeatherAPI::test_get_weather_data_valid_city -v
```

### Copertura Test

```
✅ 29 test totali - TUTTI PASSATI
✅ Validazione input completa (tipo + contenuto + pulizia)
✅ Gestione errori API verificata (Timeout, Connection, HTTP, JSON, Key)
✅ Timeout configurabile e logging testati
✅ Mappatura weathercode completa (25+ condizioni)
✅ Parsing JSON sicuro con fallback
✅ Input non-valido (None, int, list, spazi) gestito
```

---

## 📁 Struttura Progetto

```
weather_app/
├── src/
│   ├── __init__.py         # Inizializzazione package
│   ├── main.py             # Punto di ingresso principale
│   ├── weather_api.py      # Logica API e geocoding
│   ├── display.py          # Formattazione output
│   └── models.py           # Modello dati WeatherData
├── tests/
│   ├── __init__.py         # Inizializzazione test package
│   └── test_weather_api.py # Suite di test completa
├── requirements.txt        # Dipendenze progetto
└── README.md              # Questo file
```

---

## 🤝 Contributi

I contributi sono benvenuti! Se desideri migliorare l'app, sentiti libero di aprire una pull request o segnalare problemi.

---

## 📝 Licenza

ITA:

COMPONENTI DI TERZE PARTI E LICENZE

Questa applicazione utilizza le seguenti librerie e servizi di terze parti:

1. Tkinter
Parte della distribuzione standard di Python.
Distribuito sotto la Python Software Foundation License (PSF License).

2. ttkbootstrap
Distribuito sotto licenza MIT.
Copyright (c) contributori di ttkbootstrap.

3. Requests
Distribuito sotto licenza Apache License 2.0.
Copyright (c) Kenneth Reitz.

4. Moduli della libreria standard di Python
I seguenti moduli fanno parte di Python e sono coperti dalla PSF License:
- logging
- re
- sys
- os

5. Open-Meteo API
Questa applicazione utilizza dati meteorologici forniti da Open-Meteo.

Attribuzione:
Weather data by Open-Meteo.com (https://open-meteo.com/)

I dati meteorologici possono essere basati su fonti open multiple.
L’uso dell’API è soggetto ai termini di utilizzo di Open-Meteo.

--------------------------------------------------------------------

NOTE

Tutti i componenti di terze parti mantengono i rispettivi diritti d'autore.
Questa applicazione non è affiliata né sponsorizzata dai progetti sopra citati.
L’utente finale è responsabile del rispetto delle licenze delle terze parti applicabili.

ENG:

--------------------------------------------------------------------

THIRD-PARTY COMPONENTS AND LICENSES

This application uses the following third-party libraries and services:

1. Tkinter
Part of the standard distribution of Python.
Licensed under the Python Software Foundation License (PSF License).

2. ttkbootstrap
Licensed under the MIT License.
Copyright (c) ttkbootstrap contributors.

3. Requests
Licensed under the Apache License 2.0.
Copyright (c) Kenneth Reitz.

4. Python Standard Library Modules
The following modules are part of Python and are licensed under the PSF License:
- logging
- re
- sys
- os

5. Open-Meteo API
This application uses weather data provided by Open-Meteo.

Attribution:
Weather data by Open-Meteo.com (https://open-meteo.com/)

Weather data may be based on open data from multiple sources.
Use of the API is subject to Open-Meteo terms of service.

--------------------------------------------------------------------

NOTES

All third-party components retain their respective copyrights.
This application is not affiliated with or endorsed by any of the above projects.
The end user is responsible for complying with applicable third-party licenses.

---

## 📞 Supporto

Per domande o problemi, apri un issue nel repository del progetto.

---

**Buon utilizzo! 🌍**
