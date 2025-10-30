import json
import re
import time
from datetime import datetime

import matplotlib
import matplotlib.pyplot as plt
import toml
from meteofrance_api import MeteoFranceClient

matplotlib.use("Agg")  # Use non-GUI backend


class WeatherApp:
    def __init__(self):
        self.client = MeteoFranceClient()
        self.config = self.load_config()
        self.favorites = self.load_favorites()
        self.cache = {}
        self.CACHE_DURATION = 900

    def load_config(self):
        try:
            return toml.load("config.toml")
        except FileNotFoundError:
            return {"units": {"temperature": "C", "wind_speed": "km/h", "precipitation": "mm"}}

    def load_favorites(self):
        try:
            with open("favorites.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def save_favorites(self):
        with open("favorites.json", "w") as f:
            json.dump(self.favorites, f)

    def convert_temperature(self, temp, unit):
        if unit == "F":
            return temp * 9 / 5 + 32
        return temp

    def convert_wind_speed(self, speed, unit):
        if unit == "mph":
            return speed * 0.621371
        return speed

    def convert_precipitation(self, precip, unit):
        if unit == "in":
            return precip * 0.0393701
        return precip

    def get_cached_forecast(self, place):
        cache_key = (place.latitude, place.longitude)
        now = time.time()
        if cache_key in self.cache and now - self.cache[cache_key][0] < self.CACHE_DURATION:
            return self.cache[cache_key][1]
        forecast = self.client.get_forecast_for_place(place)
        self.cache[cache_key] = (now, forecast)
        return forecast

    def display_current_weather(self, current, position):
        temp_unit = self.config["units"]["temperature"]
        wind_unit = self.config["units"]["wind_speed"]
        precip_unit = self.config["units"]["precipitation"]
        temp = self.convert_temperature(current["T"]["value"], temp_unit)
        wind_speed = self.convert_wind_speed(current["wind"]["speed"], wind_unit)
        rain = (
            self.convert_precipitation(current["rain"]["1h"], precip_unit)
            if "1h" in current["rain"]
            else 0
        )
        print("\n=== Current Weather ===")
        print(f"Temperature: {temp:.1f}°{temp_unit}")
        print(f"Humidity: {current['humidity']}%")
        print(f"Wind: {wind_speed:.1f} {wind_unit} {current['wind']['direction']}°")
        print(f"Rain (last hour): {rain:.1f} {precip_unit}")
        print(f"Weather: {current['weather']['desc']}")

    def display_hourly_forecast(self, hourly_forecast):
        temp_unit = self.config["units"]["temperature"]
        wind_unit = self.config["units"]["wind_speed"]
        precip_unit = self.config["units"]["precipitation"]
        print("\n=== Hourly Forecast (Next 24 hours) ===")
        for hour in hourly_forecast[:24]:
            time_str = datetime.fromtimestamp(hour["dt"]).strftime("%Y-%m-%d %H:%M")
            temp = self.convert_temperature(hour["T"]["value"], temp_unit)
            wind_speed = self.convert_wind_speed(hour["wind"]["speed"], wind_unit)
            rain_1h = self.convert_precipitation(hour["rain"].get("1h", 0), precip_unit)
            print(
                f"{time_str}: {temp:.1f}°{temp_unit}, Humidity: {hour['humidity']}%, "
                f"Wind: {wind_speed:.1f} {wind_unit} {hour['wind']['direction']}°, "
                f"Rain: {rain_1h:.1f} {precip_unit}, Weather: {hour['weather']['desc']}"
            )

    def display_daily_forecast(self, daily_forecast):
        temp_unit = self.config["units"]["temperature"]
        precip_unit = self.config["units"]["precipitation"]
        print("\n=== Daily Forecast ===")
        for day in daily_forecast:
            date = datetime.fromtimestamp(day["dt"]).strftime("%Y-%m-%d")
            temp_min = (
                self.convert_temperature(day["T"]["min"], temp_unit)
                if day["T"]["min"] is not None
                else "N/A"
            )
            temp_max = (
                self.convert_temperature(day["T"]["max"], temp_unit)
                if day["T"]["max"] is not None
                else "N/A"
            )
            precip = (
                self.convert_precipitation(day["precipitation"]["24h"], precip_unit)
                if day["precipitation"]["24h"] is not None
                else 0
            )
            weather_desc = day["weather12H"]["desc"] if day["weather12H"] else "N/A"
            uv = day["uv"] if day["uv"] is not None else "N/A"
            print(
                f"{date}: {temp_min}°{temp_unit if temp_min != 'N/A' else ''} - "
                f"{temp_max}°{temp_unit if temp_max != 'N/A' else ''}, "
                f"Precip: {precip:.1f} {precip_unit}, Weather: {weather_desc}, UV: {uv}"
            )

    def display_observations(self, place):
        try:
            obs = self.client.get_observation_for_place(place)
            temp_unit = self.config["units"]["temperature"]
            wind_unit = self.config["units"]["wind_speed"]
            temp_obs = self.convert_temperature(obs.temperature, temp_unit)
            wind_obs = self.convert_wind_speed(obs.wind_speed, wind_unit)
            print("\n=== Observations (Station Météo) ===")
            print(f"Station: Proche ({place.name})")
            print(f"Temperature: {temp_obs:.1f}°{temp_unit}")
            print(f"Wind: {wind_obs:.1f} {wind_unit} {obs.wind_direction}°")
            print(f"Description: {obs.weather_description}")
            print(f"Time: {obs.time_as_string}")
        except Exception as e:
            print(f"\nObservations non disponibles : {e}")

    def display_picture(self):
        try:
            pic = self.client.get_picture_of_the_day()
            print("\n=== Picture of the Day ===")
            print(f"URL: {pic.image_url}")
            print(f"Description: {pic.description}")
        except Exception as e:
            print(f"\nImage du jour non disponible : {e}")

    def display_warnings(self, position):
        try:
            domain = position["dept"]
            warn = self.client.get_warning_current_phenomenons(domain)
            wd = self.client.get_warning_dictionary()
            print("\n=== Weather Warnings ===")
            if warn.phenomenons_max_colors:
                for item in warn.phenomenons_max_colors:
                    phenom_id = int(item["phenomenon_id"])
                    color_id = int(item["phenomenon_max_color_id"])
                    phenom_name = wd.get_phenomenon_name_by_id(phenom_id)
                    color_name = wd.get_color_name_by_id(color_id)
                    print(f"{phenom_name}: Niveau {color_name} (ID {phenom_id})")
            else:
                print("Aucune alerte actuelle.")
        except Exception as e:
            print(f"\nAlertes météo non disponibles : {e}")

    def display_warning_dict(self):
        try:
            wd = self.client.get_warning_dictionary()
            print("\n=== Warning Dictionary (Exemples) ===")
            example_ids = [1, 2, 3]
            for id in example_ids:
                try:
                    name = wd.get_phenomenon_name_by_id(id)
                    color_name = wd.get_color_name_by_id(id)
                    print(f"ID {id}: {name} - {color_name}")
                except (KeyError, AttributeError):
                    pass
        except Exception as e:
            print(f"\nDictionnaire d'alertes non disponible : {e}")

    def display_rain_forecast(self, position, place):
        if position["rain_product_available"] == 1:
            rain_forecast = self.client.get_rain(place.latitude, place.longitude)
            print("\n=== Rain Forecast ===")
            next_rain_dt = rain_forecast.next_rain_date_locale()
            if not next_rain_dt:
                rain_status = "No rain expected in the following hour."
            else:
                rain_status = f"Next rain at {next_rain_dt.strftime('%H:%M')}"
            print(f"Rain status: {rain_status}")
        else:
            print("\nNo rain forecast available.")

    def generate_graph(self, hourly_forecast, position):
        temp_unit = self.config["units"]["temperature"]
        times = []
        temps = []
        for hour in hourly_forecast[:24]:
            times.append(datetime.fromtimestamp(hour["dt"]))
            temps.append(self.convert_temperature(hour["T"]["value"], temp_unit))

        plt.figure(figsize=(10, 5))
        plt.plot(times, temps, marker="o")
        plt.title(f"Prévisions de température pour {position['name']}")
        plt.xlabel("Heure")
        plt.ylabel(f"Température (°{temp_unit})")
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        plt.savefig("weather_graph.png")
        plt.close()
        print("Graphique sauvegardé dans 'weather_graph.png'.")

    def run(self):
        print(
            """
███╗   ███╗███████╗████████╗███████╗ ██████╗     ███████╗██████╗  █████╗ ███╗   ██╗ ██████╗███████╗
████╗ ████║██╔════╝╚══██╔══╝██╔════╝██╔═══██╗    ██╔════╝██╔══██╗██╔══██╗████╗  ██║██╔════╝██╔════╝
██╔████╔██║█████╗     ██║   █████╗  ██║   ██║    █████╗  ██████╔╝███████║██╔██╗ ██║██║     █████╗
██║╚██╔╝██║██╔══╝     ██║   ██╔══╝  ██║   ██║    ██╔══╝  ██╔══██╗██╔══██║██║╚██╗██║██║     ██╔══╝
██║ ╚═╝ ██║███████╗   ██║   ███████╗╚██████╔╝    ██║     ██║  ██║██║  ██║██║ ╚████║╚██████╗███████╗
╚═╝     ╚═╝╚══════╝   ╚═╝   ╚══════╝ ╚═════╝     ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝╚══════╝
"""
        )

        while True:
            print("\nVilles favorites:")
            for i, fav in enumerate(self.favorites, 1):
                region = fav.get("region", "")
                dept = fav.get("dept", "")
                display = f"{fav['name']}"
                if region:
                    display += f" - {region}"
                if dept:
                    display += f" ({dept})"
                print(f"{i}. {display}")
            print(f"{len(self.favorites) + 1}. Nouvelle ville")

            try:
                choice = int(input("Choisissez un numéro : "))
                if 1 <= choice <= len(self.favorites):
                    fav_data = self.favorites[choice - 1]
                    my_place = type("Place", (), fav_data)()
                    search_city = fav_data["name"]
                    add_to_fav = False
                elif choice == len(self.favorites) + 1:
                    city = input("Entrez le nom de la ville : ").strip()
                    if not city:
                        print("Veuillez entrer un nom de ville valide.")
                        continue
                    search_city = city
                    add_to_fav = True
                else:
                    print("Numéro invalide.")
                    continue
            except ValueError:
                print("Veuillez entrer un numéro valide.")
                continue

            if add_to_fav:
                list_places = self.client.search_places(search_city)
                if not list_places:
                    print(f"Aucun lieu trouvé pour '{search_city}'. Réessayez.")
                    continue

                print(f"\nLieux trouvés pour '{search_city}':")
                for i, place in enumerate(list_places, 1):
                    print(f"{i}. {place}")

                while True:
                    try:
                        choice = int(input(f"\nChoisissez un numéro (1-{len(list_places)}) : "))
                        if 1 <= choice <= len(list_places):
                            my_place = list_places[choice - 1]
                            break
                        else:
                            print(f"Numéro invalide. Choisissez entre 1 et {len(list_places)}.")
                    except ValueError:
                        print("Veuillez entrer un numéro valide.")

                place_str = str(my_place)

                dept_match = re.search(r"\((\d+)\)", place_str)
                dept = dept_match.group(1) if dept_match else ""
                region_match = re.search(r" - (.+?) \(", place_str)
                region = region_match.group(1) if region_match else ""
                fav_data = {
                    "name": my_place.name,
                    "region": region,
                    "dept": dept,
                    "latitude": my_place.latitude,
                    "longitude": my_place.longitude,
                    "country": my_place.country,
                    "insee": getattr(my_place, "insee", ""),
                }
                if fav_data not in self.favorites:
                    self.favorites.append(fav_data)
                    self.save_favorites()
                    print("Ajouté aux favoris.")

            # Get forecast
            try:
                forecast = self.get_cached_forecast(my_place)
                position = forecast.position
                print("\n=== Weather Forecast for ===")
                print(f"Location: {position['name']}, {position['dept']} - {position['country']}")
                print(f"Coordinates: {position['lat']:.4f}, {position['lon']:.4f}")
                print(f"Elevation: {position['alti']}m")
                print(f"Timezone: {position['timezone']}")

                # Current weather
                current = forecast.current_forecast
                if current:
                    self.display_current_weather(current, position)

                # Sunrise/Sunset
                first_day = forecast.daily_forecast[0]
                sunrise = datetime.fromtimestamp(first_day["sun"]["rise"]).strftime("%H:%M")
                sunset = datetime.fromtimestamp(first_day["sun"]["set"]).strftime("%H:%M")
                print(f"\nSunrise: {sunrise}, Sunset: {sunset}")

                # Warnings
                probability = forecast.probability_forecast
                if probability:
                    print("\n=== Weather Warnings ===")
                    for prob in probability:
                        if prob.get("probability", 0) > 0:
                            print(f"{prob.get('type', 'Unknown')}: {prob['probability']}%")

                # Forecasts
                self.display_hourly_forecast(forecast.forecast)
                self.display_daily_forecast(forecast.daily_forecast)

                # Additional data
                self.display_observations(my_place)
                self.display_picture()
                self.display_warnings(position)
                self.display_warning_dict()
                self.display_rain_forecast(position, my_place)

                # Graph
                show_graph = (
                    input("\nVoulez-vous voir un graphique des températures horaires ? (o/n) : ")
                    .strip()
                    .lower()
                )
                if show_graph == "o":
                    self.generate_graph(forecast.forecast, position)

            except Exception as e:
                print(f"Erreur lors de la récupération des données : {e}")

            another = input("\nVoulez-vous rechercher une autre ville ? (o/n) : ").strip().lower()
            if another != "o":
                break


if __name__ == "__main__":
    app = WeatherApp()
    app.run()


def main():
    """Point d'entrée pour l'exécution en tant que module."""
    app = WeatherApp()
    app.run()
