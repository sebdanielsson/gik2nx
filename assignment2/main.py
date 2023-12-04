# Use https://www.wunderground.com/weather/se/borlänge for Assignment
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from bs4 import BeautifulSoup
from kivy.properties import StringProperty
import requests


class HomeScreen(Screen):
    weather = StringProperty()
    description = StringProperty()
    humidity = StringProperty()
    pressure = StringProperty()
    visibility = StringProperty()

    def search(self, country, city):
        # Get the country and city name from the text fields
        country = country.lower()
        city = city.lower()

        # Debug print
        print("Country: ", country)
        print("City: ", city)

        # Set the country value for the websites
        if country == 'sweden':
            timeanddate_country = 'sweden'
            wunderground_country = 'se'
        else:
            timeanddate_country = country
            wunderground_country = country
        
        # Create another variable for city name without å ä ö
        timeanddate_city = city.replace('å', 'a').replace('ä', 'a').replace('ö', 'o')

        # Set the url for the websites
        timeanddate_url = f'https://www.timeanddate.com/weather/{timeanddate_country}/{timeanddate_city}'
        wunderground_url = f'https://www.wunderground.com/weather/{wunderground_country}/{city}'

        # Try to get data from timeanddate.com if it fails, try wunderground.com
        try:
            response = requests.get(url=timeanddate_url)
            if response.status_code >= 200 and response.status_code < 300:
                soup = BeautifulSoup(response.text,'html.parser')
                mainclass = soup.find(class_='bk-focus__qlook')
                secondclass = soup.find(class_='bk-focus__info')
                self.weather = mainclass.find(class_='h2').get_text()
                self.visibility = secondclass.findAll('td')[3].get_text()  # can also try slicing
                self.pressure = secondclass.findAll('td')[4].get_text()
                self.humidity = secondclass.findAll('td')[5].get_text()
            else:
                print("Failed to retrieve weather data from timeanddate.com")
                response = requests.get(url=wunderground_url)
                if response.status_code >= 200 and response.status_code < 300:
                    print("Status code: ", response.status_code)
                    soup = BeautifulSoup(response.text,'html.parser')
                    mainclass = soup.find(class_='h1')

                else:
                    print("Failed to retrieve weather data from wunderground.com")
        except requests.exceptions.RequestException as e:
            print("An error occurred:", e)


class MainApp(MDApp):
    def build(self, **kwargs):
        self.theme_cls.theme_style = "Dark"
        Window.size = (400, 600)


MainApp().run()
