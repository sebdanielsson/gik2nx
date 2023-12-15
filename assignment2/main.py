from kivy.config import Config
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.properties import NumericProperty, StringProperty
from kivymd.app import MDApp
from kivymd.toast import toast
from bs4 import BeautifulSoup
import requests
import json
import datetime

class MainApp(MDApp):
    firebase_url_1 = 'https://gik2nx-assignment2-6efca-default-rtdb.europe-west1.firebasedatabase.app/.json'
    firebase_url_2 = 'https://assignment2-a756d-default-rtdb.firebaseio.com/.json'
    allow_save = False
    temperature = StringProperty(' ')
    humidity = StringProperty(' ')
    pressure = StringProperty(' ')
    visibility = StringProperty(' ')

    def build(self):
        #  self.theme_cls.theme_style = "Dark"
        Window.size = (360, 600)
        return Builder.load_file('main.kv')

    # Clear the text fields and the weather data
    def clear(self):
        self.temperature = ' '
        self.humidity = ' '
        self.pressure = ' '
        self.visibility = ' '
        self.root.ids.country.text = ''
        self.root.ids.city.text = ''

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

        headers = {
                'Accept-Language': 'sv',
                'Accept-Region': 'se',
            }

        # Try to get data from timeanddate.com if it fails, try wunderground.com
        try:
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
                if response_wunderground.status_code >= 200 and response_wunderground.status_code < 300:
                    soup = BeautifulSoup(response_wunderground.text,'html.parser')

                    # If the city does not exist, the website will return a page containing the text ', undefined'
                    if soup.find_all(class_='station-state')[0].text == ', undefined':
                        toast("City does not exist")
                        print("City does not exist")
                        return

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

    def save_to_db(self, country, city):
        utc_time = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        
        if self.temperature == ' ' or self.temperature == '':
            toast("No data to save")
            return
        elif self.allow_save == False:
            toast("Data already saved")
            return

        print("Saving data to database")
        json_data = '{"'+country+'-'+city+' '+utc_time+'":{"Temperature": "'+self.temperature+'", "Visibility": "'+self.visibility+'", "Pressure": "'+self.pressure+'", "Humidity": "'+self.humidity+'"}}'
        res=requests.post(url=self.firebase_url_1, json=json.loads(json_data))
        res=requests.post(url=self.firebase_url_2, json=json.loads(json_data))
        print(res)
        self.allow_save = False

if __name__ == '__main__':
    MainApp().run()
