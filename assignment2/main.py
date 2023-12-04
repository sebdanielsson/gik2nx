from kivy.config import Config
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.properties import NumericProperty, StringProperty
from kivymd.app import MDApp
from kivymd.toast import toast
from bs4 import BeautifulSoup
import requests
import json

Config.set('graphics', 'width', str(420))
Config.set('graphics', 'height', str(980))

class MainApp(MDApp):
    firebase_url = 'https://gik2nx-assignment2-6efca-default-rtdb.europe-west1.firebasedatabase.app/.json'
    allow_save = False

    temperature = StringProperty('')
    humidity = StringProperty('')
    pressure = StringProperty('')
    visibility = StringProperty('')

    def build(self):
        #self.theme_cls.theme_style = "Dark"
        Window.size = (400, 600)
        return Builder.load_file('main.kv')

    def search(self, country, city):
        # Make sure that the user has filled in both fields
        if not country or not city:
            toast("Please fill in both search fields.")
            return

        # Get the country and city name from the text fields
        country = country.lower()
        city = city.lower()

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
            headers = {
                'Accept-Language': 'sv',
                'Accept-Region': 'se',
            }
            response_timeanddate = requests.get(url=timeanddate_url, headers=headers)
            response_wunderground = requests.get(url=wunderground_url, headers=headers)
            if response_timeanddate.status_code >= 200 and response_timeanddate.status_code < 300:
                soup = BeautifulSoup(response_timeanddate.text,'html.parser')
                mainclass = soup.find(class_='bk-focus__qlook')
                secondclass = soup.find(class_='bk-focus__info')

                self.temperature = mainclass.find('div', class_='h2').get_text()
                self.visibility = secondclass.findAll('td')[3].get_text()
                self.pressure = secondclass.findAll('td')[4].get_text()
                self.humidity = secondclass.findAll('td')[5].get_text()
            else:
                print("Failed to retrieve weather data from timeanddate.com")
                headers = {
                    'Accept-Language': 'sv',
                    'Accept-Region': 'se',
                }
                if response_wunderground.status_code >= 200 and response_wunderground.status_code < 300:
                    soup = BeautifulSoup(response_wunderground.text,'html.parser')
                    temp_circle = soup.find_all(class_='test-true wu-unit wu-unit-temperature is-degree-visible ng-star-inserted')[0]
                    additional_conditions = soup.find(class_='additional-conditions')

                    self.temperature = temp_circle.find_all('span')[0].text + temp_circle.find_all('span')[1].text
                    self.visibility = additional_conditions.find_all(class_='row')[1].find_all('div')[1].get_text().replace(u'\xb0', '')
                    self.pressure = additional_conditions.find_all(class_='row')[0].find_all('div')[1].get_text().replace(u'\xb0', '')
                    self.humidity = additional_conditions.find_all(class_='row')[4].find_all('div')[1].get_text().replace(u'\xb0', '')
                else:
                    print("Failed to retrieve weather data from wunderground.com")
            self.allow_save = True
        except requests.exceptions.RequestException as e:
            print("An error occurred:", e)

    # Clear the text fields (No button added yet)
    def clear(self):
        self.temperature = ''
        self.humidity = ''
        self.pressure = ''
        self.visibility = ''
        self.root.ids.country.text = ''
        self.root.ids.city.text = ''

    def save_to_db(self):
        if self.temperature == '':
            toast("No data to save")
            return
        elif self.allow_save == False:
            toast("Data already saved")
            return

        print("Saving data database")
        json_data = '{"SavedWeatherData":{"Temperature": "'+self.temperature+'", "Visibility": "'+self.visibility+'", "Pressure": "'+self.pressure+'", "Humidity": "'+self.humidity+'"}}'
        res=requests.post(url=self.firebase_url, json=json.loads(json_data))
        print(res)
        self.allow_save = False

if __name__ == '__main__':
    MainApp().run()
