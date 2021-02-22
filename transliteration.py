def transliteration_data(data):
    transliteration_letters = {
        'а': 'a',
        'б': 'b',
        'в': 'v',
        'г': 'g',
        'д': 'd',
        'е': 'e',
        'ж': 'zh',
        'з': 'z',
        'и': 'i',
        'й': 'y',
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
        'х': 'h',
        'ц': 'c',
        'ч': 'ch',
        'ш': 'sh',
        'щ': 'sh',
        'ъ': '',
        'ь': '',
        'ы': 'i',
        'э': 'e',
        'ю': 'u',
        'я': 'ya',
        ' ': '_'}

    translit_data = data.lower()
    if translit_data == 'москва':
        return 'msk'
    elif translit_data == 'санкт-петербург':
        return 'spb'
    elif translit_data == 'астрахань':
        return 'astrakhan'
    else:
        for key in transliteration_letters:
            translit_data = translit_data.replace(key, transliteration_letters[key])
        return translit_data.lower()