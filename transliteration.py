def transliteration_for_city(city):
    transliteration_letters = {
        'а': 'a',
        'б': 'b',
        'в': 'v',
        'г': 'g',
        'д': 'd',
        'е': 'e',
        'ё': 'e',
        'ж': 'zh',
        'з': 'z',
        'и': 'i',
        'й': 'i',
        'к': 'k',
        'л': 'l',
        'м': 'm',
        'н': 'n',
        'о': 'o',
        'п': 'p',
        'р': 'r',
        'с': 's',
        'т': 't',
        'у': 'u',
        'ф': 'f',
        'х': 'kh',
        'ц': 'c',
        'ч': 'ch',
        'ш': 'sh',
        'щ': 'scz',
        'ъ': '',
        'ы': 'y',
        'ь': '',
        'э': 'e',
        'ю': 'u',
        'я': 'ja'}

    translit_city = city.lower()
    for key in transliteration_letters:
        translit_city = translit_city.replace(key, transliteration_letters[key])
    return translit_city.lower()
