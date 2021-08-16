"""Реализовать функционал получения информации о городе посредством Python.

User Story: При запуске файла пользователь вводит название города, система возвращает название города, страну, валюту и
количество населения

Tech Requirements:
    -Ввод реализовать с помощью CLI интерфейса. Выбор WEB-API для получения информации - на усмотрение разработчика.
    -Код должен быть читаемым, с комментариями и соответствовать принципам DRY, KISS, YAGNI.
    -Кд должен быть загружен на GitHub или GitLab как отдельный проект с публичным доступом.
    -Формат вывода только такой как в примере"""

import requests
import time


class CityDataBot:
    """Class of Bot, that will show you the information about city, which name will be inputed"""
    def __init__(self, city):
        self.city = str(city)

    @staticmethod
    def currency(country_code: str):
        """Takes the country code from 'show_info' and return a currency of one"""
        url = "https://wft-geo-db.p.rapidapi.com/v1/geo/countries/" + country_code
        headers = {
            'x-rapidapi-key': "21c453a4d6mshf97b6774430c674p1b1149jsn804d3d516f1a",
            'x-rapidapi-host': "wft-geo-db.p.rapidapi.com"
        }
        try:
            response = requests.request("GET", url, headers=headers, timeout=5).json()
        except Exception:
            return '--------------\nSystem Error\n=============='

        return response['data']['currencyCodes'][0]

    def show_info(self):
        """Main function, does  request to the API, forming the result"""
        url = "https://wft-geo-db.p.rapidapi.com/v1/geo/cities"
        querystring = {"namePrefix": self.city}
        headers = {
            'x-rapidapi-key': "21c453a4d6mshf97b6774430c674p1b1149jsn804d3d516f1a",
            'x-rapidapi-host': "wft-geo-db.p.rapidapi.com"
        }

        try:
            response = requests.request("GET", url, headers=headers, params=querystring, timeout=5).json()
        except Exception:
            return '--------------\nSystem Error\n=============='

        if response['metadata']['totalCount'] == 0:
            return f'--------------\n{self.city}\n\nInvalid city name: {self.city}\n=============='
        response = response['data']

        res = ''
        for item in response:
            time.sleep(1.5)  # Since the api doesn't allow more than 1 request per second
            res += str('--------------\n' + self.city + '\n\n' + item['country'] + '\n' +
                       CityDataBot.currency(item['countryCode']) + '\n' + str(item['population']) +
                       '\n' + '==============\n')

        return res

    @staticmethod
    def main():
        """Launcher"""
        data = input().capitalize()
        data = CityDataBot(data)
        return data.show_info()


print(CityDataBot.main())