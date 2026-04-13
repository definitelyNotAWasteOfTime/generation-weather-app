import sys
import os
# Aggiungi il path del progetto al sys.path per import assoluti
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import tkinter as tk
from tkinter import messagebox
from ttkbootstrap import Style, ttk
from src.weather_api import get_weather_data
from src.models import WeatherData

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🌤️ Meteo App")
        self.root.geometry("700x580")
        self.root.resizable(True, True)
        self.root.minsize(520, 420)

        # Stili moderni con ttkbootstrap
        self.style = Style(theme="flatly")
        self.style.configure("Main.TFrame", background="#e9f1ff")
        self.style.configure("Hero.TFrame", background="#1f5a8a")
        self.style.configure("Hero.TLabel", background="#1f5a8a", foreground="#ffffff",
                             font=("Helvetica", 18, "bold"), padding=12)
        self.style.configure("Hero.SubLabel.TLabel", background="#1f5a8a", foreground="#d7e4ff",
                             font=("Helvetica", 10), padding=(0, 0, 0, 10))
        self.style.configure("Card.TFrame", background="#ffffff", relief="flat", borderwidth=0)
        self.style.configure("CardBorder.TFrame", background="#ffffff", relief="solid", borderwidth=1)
        self.style.configure("CardTitle.TLabel", background="#ffffff", foreground="#1f5a8a",
                             font=("Helvetica", 12, "bold"))
        self.style.configure("BigValue.TLabel", background="#ffffff", foreground="#15345b",
                             font=("Helvetica", 44, "bold"))
        self.style.configure("SmallValue.TLabel", background="#ffffff", foreground="#2d5d8b",
                             font=("Helvetica", 11, "bold"))
        self.style.configure("Detail.TLabel", background="#ffffff", foreground="#5f728b",
                             font=("Helvetica", 10))
        self.style.configure("Footer.TLabel", background="#e9f1ff", foreground="#475c75",
                             font=("Helvetica", 10))

        self.root.configure(bg="#e9f1ff")
        self.root.grid_rowconfigure(0, weight=0)
        self.root.grid_rowconfigure(1, weight=0)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_rowconfigure(3, weight=0)
        self.root.grid_columnconfigure(0, weight=1)

        # Hero header
        hero_frame = ttk.Frame(root, style="Hero.TFrame")
        hero_frame.grid(row=0, column=0, sticky="ew")
        hero_frame.grid_columnconfigure(0, weight=1)
        hero_title = ttk.Label(hero_frame, text="Previsioni meteo rapide", style="Hero.TLabel", anchor="w")
        hero_title.grid(row=0, column=0, padx=20, sticky="ew")
        hero_subtitle = ttk.Label(hero_frame, text="Inserisci la città e ottieni le condizioni attuali in tempo reale.", style="Hero.SubLabel", anchor="w")
        hero_subtitle.grid(row=1, column=0, padx=20, sticky="ew")

        # Search card
        search_card = ttk.Frame(root, style="CardBorder.TFrame")
        search_card.grid(row=1, column=0, pady=18, padx=20, sticky="ew")
        search_card.grid_columnconfigure(1, weight=1)
        search_card.grid_columnconfigure(2, weight=0)

        search_title = ttk.Label(search_card, text="Cerca la tua località", style="CardTitle.TLabel")
        search_title.grid(row=0, column=0, columnspan=3, padx=20, pady=(18, 10), sticky="w")

        city_label = ttk.Label(search_card, text="📍 Città", style="Detail.TLabel")
        city_label.grid(row=1, column=0, padx=(20, 10), pady=6, sticky="w")

        self.city_entry = ttk.Entry(search_card, bootstyle="info", font=("Helvetica", 12))
        self.city_entry.grid(row=1, column=1, padx=(0, 10), pady=6, sticky="ew", ipady=5)
        self.city_entry.bind("<Return>", lambda event: self.get_weather())

        self.get_weather_button = ttk.Button(search_card, text="🔍 Cerca meteo", command=self.get_weather,
                                             bootstyle="primary", width=18)
        self.get_weather_button.grid(row=1, column=2, padx=(0, 20), pady=6, sticky="e")

        # Results card
        result_card = ttk.Frame(root, style="CardBorder.TFrame")
        result_card.grid(row=2, column=0, pady=(0, 20), padx=20, sticky="nsew")
        result_card.grid_rowconfigure(0, weight=0)
        result_card.grid_rowconfigure(1, weight=1)
        result_card.grid_columnconfigure(0, weight=1)

        result_header = ttk.Frame(result_card, style="Card.TFrame")
        result_header.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        result_header.grid_columnconfigure(0, weight=1)
        self.location_label = ttk.Label(result_header, text="📍 Località non selezionata", style="CardTitle.TLabel", anchor="w")
        self.location_label.grid(row=0, column=0, sticky="w")

        result_main = ttk.Frame(result_card, style="Card.TFrame")
        result_main.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        result_main.grid_rowconfigure(0, weight=1)
        result_main.grid_columnconfigure(0, weight=1)
        result_main.grid_columnconfigure(1, weight=1)

        left_panel = ttk.Frame(result_main, style="Card.TFrame")
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 12), pady=10)
        left_panel.grid_rowconfigure(0, weight=0)
        left_panel.grid_rowconfigure(1, weight=0)
        left_panel.grid_rowconfigure(2, weight=1)

        self.temperature_value = ttk.Label(left_panel, text="--°C", style="BigValue.TLabel", anchor="w")
        self.temperature_value.grid(row=0, column=0, sticky="w")
        self.condition_value = ttk.Label(left_panel, text="Condizioni meteodefault", style="SmallValue.TLabel", anchor="w")
        self.condition_value.grid(row=1, column=0, sticky="w", pady=(6, 0))
        self.source_label = ttk.Label(left_panel, text="I dati provengono da Open-Meteo", style="Detail.TLabel", anchor="w")
        self.source_label.grid(row=2, column=0, sticky="sw", pady=(18, 0))

        right_panel = ttk.Frame(result_main, style="Card.TFrame")
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(12, 0), pady=10)
        right_panel.grid_rowconfigure(0, weight=0)
        right_panel.grid_rowconfigure(1, weight=0)
        right_panel.grid_rowconfigure(2, weight=0)
        right_panel.grid_rowconfigure(3, weight=0)
        right_panel.grid_columnconfigure(0, weight=1)

        detail_items = [
           # ("🌡️ Temperatura", "-- °C"),
            ("💧 Umidità", "-- %"),
            ("💨 Vento", "-- km/h"),
            #("🌬️ Pressione", "-- hPa"),
        ]

        self.detail_labels = []
        for index, (label, value) in enumerate(detail_items, start=0):
            item_frame = ttk.Frame(right_panel, style="CardBorder.TFrame")
            item_frame.grid(row=index, column=0, sticky="ew", pady=6)
            item_frame.grid_columnconfigure(0, weight=1)
            item_frame.grid_columnconfigure(1, weight=0)
            ttk.Label(item_frame, text=label, style="Detail.TLabel").grid(row=0, column=0, sticky="w", padx=12, pady=10)
            value_label = ttk.Label(item_frame, text=value, style="SmallValue.TLabel")
            value_label.grid(row=0, column=1, sticky="e", padx=12)
            self.detail_labels.append(value_label)

        self.humidity_value = self.detail_labels[0]
        self.wind_value = self.detail_labels[1]
        #self.pressure_value = self.detail_labels[2]

        # Label per errore con stile migliorato
        self.error_label = ttk.Label(root, text="", bootstyle="danger", 
                                     font=("Helvetica", 10, "italic"), wraplength=560,
                                     justify="center")
        self.error_label.grid(row=3, column=0, pady=(0, 20), padx=20, sticky="ew")

    def get_weather(self):
        city = self.city_entry.get().strip()
        if not city:
            self.error_label.config(text="❌ Nome città non valido. Inserisci una stringa non vuota.")
            self._clear_result_fields()
            return

        data = get_weather_data(city)

        if 'error' in data:
            self.error_label.config(text=f"❌ {data['error']}")
            self._clear_result_fields()
        else:
            weather = WeatherData(**data)
            self.location_label.config(text=f"📍 LOCALITÀ: {weather.city.upper()}")
            self.temperature_value.config(text=f"{weather.temperature:.1f}°C")
            self.condition_value.config(text=weather.condition)
            self.humidity_value.config(text=f"{weather.humidity}%")
            self.wind_value.config(text=f"{weather.wind_speed:.1f} km/h")
            self.source_label.config(text="Dati aggiornati in tempo reale da Open-Meteo")
            self.error_label.config(text="")
            self.city_entry.delete(0, tk.END)  # Clear the entry

    def _clear_result_fields(self):
        self.location_label.config(text="📍 LOCALITÀ:")
        self.temperature_value.config(text="")
        self.condition_value.config(text="")
        self.humidity_value.config(text="")
        self.wind_value.config(text="")
        self.source_label.config(text="")


def main():
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()