def search_file_with_cites(letter):
    with open('city.txt', 'r', encoding='utf-8') as cities:
        for city in cities:
            city = city[:-1]
            if city.startswith(letter):
                yield city


def look_all_cities():
    with open('city.txt', 'r', encoding='utf-8') as cities:
        for city in cities:
            city = city[:-1]
            yield city
