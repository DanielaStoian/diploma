import requests,json

def getProtergiaCharge():

    cookies = {
        'google_usage_consent': 'true',
    }

    headers = {
        'authority': 'stationmapper.htb.services',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        # 'cookie': 'google_usage_consent=true',
        'origin': 'https://stationmapper.htb.services',
        'referer': 'https://stationmapper.htb.services/map/protergia/',
        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    }

    json_data = {
        'coordinates': {
            'latNE': 41.4793552402126,
            'lngNE': 29.01651512167951,
            'latSW': 34.780832,
            'lngSW': 19.381752,
        },
        'filter': '',
    }

    response = requests.post(
        'https://stationmapper.htb.services/map/protergia/stations',
        cookies=cookies,
        headers=headers,
        json=json_data,
    )

    data = json.loads(response.content.decode('utf8'))

    return data
    
getProtergiaCharge()