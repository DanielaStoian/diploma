import requests,json

def getInCharge():

    cookies = {
        'OptanonAlertBoxClosed': '2023-03-09T17:17:20.092Z',
        'OptanonConsent': 'isGpcEnabled=0&datestamp=Fri+Mar+10+2023+15%3A16%3A55+GMT%2B0200+(Eastern+European+Standard+Time)&version=6.24.0&isIABGlobal=false&hosts=&consentId=e71c10ef-0407-4282-a8a2-6ae80373f357&interactionCount=1&landingPath=NotLandingPage&groups=C0004%3A0%2CC0003%3A0%2CC0002%3A0%2CC0001%3A1&geolocation=%3B&AwaitingReconsent=false',
    }

    headers = {
        'authority': 'www.nrgincharge.gr',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        # 'cookie': 'OptanonAlertBoxClosed=2023-03-09T17:17:20.092Z; OptanonConsent=isGpcEnabled=0&datestamp=Fri+Mar+10+2023+15%3A16%3A55+GMT%2B0200+(Eastern+European+Standard+Time)&version=6.24.0&isIABGlobal=false&hosts=&consentId=e71c10ef-0407-4282-a8a2-6ae80373f357&interactionCount=1&landingPath=NotLandingPage&groups=C0004%3A0%2CC0003%3A0%2CC0002%3A0%2CC0001%3A1&geolocation=%3B&AwaitingReconsent=false',
        'referer': 'https://www.nrgincharge.gr/el/xartis-fortiston',
        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    }

    response = requests.get('https://www.nrgincharge.gr/el/api/ic_chargers', cookies=cookies, headers=headers)
    
    data = json.loads(response.content.decode('utf8'))

    return data

def inCharge():
    data = getInCharge()
    data_list = []
    for station in data:
        name = station['name']
        lat = station['coords']['lat']
        long = station['coords']['lng']
        address = station['address']
        type = station['type']
        origin = 'InCharge'
        data_dict = {
            "name": name,
            "lat": str(lat),
            "long": str(long),
            "address": address,
            "type": type,
            "origin": origin,
        }
        data_list.append(data_dict)
    return data_list
