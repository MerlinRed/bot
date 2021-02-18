import requests
from bs4 import BeautifulSoup


def create_file_with_cities():
    response = requests.get('https://hramy.ru/regions/city_abc.htm')
    cities = BeautifulSoup(response.content, 'html.parser')

    list_cities = []
    for city in cities.select('TD'):
        list_cities.append(city.get_text())

    with open('city.txt', 'w', encoding='utf-8') as file:
        for i in range(0, len(list_cities), 5):
            file.write(f'{list_cities[i]}\n')


def search_file_with_cites(letter):
    with open('city.txt', 'r', encoding='utf-8') as cities:
        for city in cities:
            city = city[:-1]
            if city.startswith(letter):
                yield city


if __name__ == '__main__':
    create_file_with_cities()
