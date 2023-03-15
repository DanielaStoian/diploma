import requests,json

def getElpeFuture():
    cookies = {
        'lang': 'el',
    }

    headers = {
        'authority': 'elpefuture.gr',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'capikey': 'LFDSGSgdfgdfkmialsnlrgmilsndalgASDGDFhadsfhggs',
        # 'cookie': 'lang=el',
        'referer': 'https://elpefuture.gr/location',
        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    }

    response = requests.get('https://elpefuture.gr/main_service/api/infoinit/charging-locations', cookies=cookies, headers=headers)

    data = json.loads(response.content.decode('utf8'))

    return data

def elpeFuture():
    data = getElpeFuture()
    data_list = []
    for station in data['Data']['ChargingPoints']:
        name = station['Title']
        lat = station['X']
        long = station['Y']
        address = station['Address']
        type = ""
        for types in station["AvailableChargerTypeDetails"]:
            type += ', ' + types["Description"]
        type = type[2:]  
        origin = 'ElpeFuture'
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