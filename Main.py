"""Реализовать функционал получения информации о городе посредством Python.

User Story: При запуске файла пользователь вводит название города, система возвращает название города, страну, валюту и
количество населения

Tech Requirements:
    -Ввод реализовать с помощью CLI интерфейса. Выбор WEB-API для получения информации - на усмотрение разработчика.
    -Код должен быть читаемым, с комментариями и соответствовать принципам DRY, KISS, YAGNI.
    -Кд должен быть загружен на GitHub или GitLab как отдельный проект с публичным доступом.
    -Формат вывода только такой как в примере"""

import requests
from time import sleep
import sys


class CityDataBot:
    """Class of Bot, that will show you the information about city, which name will be inputed"""
    headers = {
        'x-rapidapi-key': "21c453a4d6mshf97b6774430c674p1b1149jsn804d3d516f1a",
        'x-rapidapi-host': "wft-geo-db.p.rapidapi.com"
    }

    def __init__(self, city):
        self.city = str(city)

    @staticmethod
    def error():
        return '--------------\nSystem Error\n=============='

    def invalid_name(self):
        return f'--------------\n{self.city}\n\nInvalid city name: {self.city}\n=============='

    @staticmethod
    def currency(country_code: str):
        """Takes the country code from 'show_info' and return a currency of one"""
        url = "https://wft-geo-db.p.rapidapi.com/v1/geo/countries/" + country_code

        try:
            response = requests.request("GET", url, headers=CityDataBot.headers, timeout=5).json()
        except requests.RequestException:
            return CityDataBot.error()

        res = response['data']['currencyCodes'][0]
        return res if res else 'No info'

    def show_info(self):
        """Main function, does  request to the API, forming the result"""
        url = "https://wft-geo-db.p.rapidapi.com/v1/geo/cities"
        querystring = {"namePrefix": self.city}

        try:
            response = requests.request("GET", url, headers=self.headers, params=querystring, timeout=5).json()
        except requests.RequestException:
            return self.error()

        if response['metadata']['totalCount'] == 0:
            return self.invalid_name()
        response = response['data']
        response = sorted(response, key=lambda x: x['population'], reverse=True)

        res = []
        for item in response:
            sleep(1.5)  # Since the api doesn't allow more than 1 request per second
            if item['population'] == 0:
                continue
            res.extend(
                [
                    '--------------\n', self.city, '\n\n', item['country'] + '\n',
                    CityDataBot.currency(item['countryCode']), '\n', str(item['population']), '\n', '==============\n'
                ]
            )

        return ' '.join(res)

    @staticmethod
    def main():
        """Launcher"""
        args = sys.argv[1:]
        data = ' '
        data = data.join(args)
        data = data.capitalize()
        data = CityDataBot(data)
        return data.show_info()


print(CityDataBot.main())
