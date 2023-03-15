import requests,json

def getPlugShare():

    headers = {
        'authority': 'api.plugshare.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en',
        'authorization': 'Basic d2ViX3YyOkVOanNuUE54NHhXeHVkODU=',
        'cognito-authorization': 'eyJraWQiOiJ4RmIzSVZuTXhYZEhUaWNTN1NJeVNGc3BHOUsydVZ2NUVNT2U4NkQxeHhBPSIsImFsZyI6IlJTMjU2In0.eyJhdF9oYXNoIjoid3NQYXhId0tzcGdZSmUwbUxaUkY4QSIsInN1YiI6ImZhOGI3ZTc3LWMxZTYtNGI2Ni04NmUyLTQ1ZjZjNjMxMDkwNyIsImN1c3RvbTpwbHVnc2hhcmVfaWQiOiIzMjg2MTgzIiwiY29nbml0bzpncm91cHMiOlsidXMtZWFzdC0xX293ZVE3WG1HZl9Hb29nbGUiXSwiZW1haWxfdmVyaWZpZWQiOnRydWUsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC51cy1lYXN0LTEuYW1hem9uYXdzLmNvbVwvdXMtZWFzdC0xX293ZVE3WG1HZiIsImNvZ25pdG86dXNlcm5hbWUiOiJnb29nbGVfMTExNDYxODYzMTc1NzU2NzcyMzc3IiwiZ2l2ZW5fbmFtZSI6IkRhbmllbGEiLCJwaWN0dXJlIjoiaHR0cHM6XC9cL2xoMy5nb29nbGV1c2VyY29udGVudC5jb21cL2FcL0FHTm15eGJobjhTMXdIQ2JfcWd3YlhwUzgzVV9fMVFrbEtlWkhIQi1JZTZVPXM5Ni1jIiwiYXVkIjoiMnUwcWkzcjBla2MzaG5zbDJyc2czMTFjaSIsImlkZW50aXRpZXMiOlt7InVzZXJJZCI6IjExMTQ2MTg2MzE3NTc1Njc3MjM3NyIsInByb3ZpZGVyTmFtZSI6Ikdvb2dsZSIsInByb3ZpZGVyVHlwZSI6Ikdvb2dsZSIsImlzc3VlciI6bnVsbCwicHJpbWFyeSI6InRydWUiLCJkYXRlQ3JlYXRlZCI6IjE2NzgzNjcwMDMzMTEifV0sInRva2VuX3VzZSI6ImlkIiwiYXV0aF90aW1lIjoxNjc4MzY3MDA1LCJuYW1lIjoiRGFuaWVsYSBTdG9pYW4iLCJleHAiOjE2Nzg0NjAwMTMsImlhdCI6MTY3ODQ1NjQxMywiZW1haWwiOiJkYW5pZS5zdG9pYW5AZ21haWwuY29tIn0.OEmR9UrGSiMC_HP1OQKtgPRLgBnbT3GsxcbchZ2dTaiU8asTA5PZwowgjm-JYHqPg9FFJ1KqdAQ4HM8MYQSKTWdXTh2dOh065-vUMbT1G3PFjEmteSaGYs-8LCWvni8PSSHLwMAF6yZABe0FKKQEptrhiKJ9IRTI1R2t1ZJA2AJS--8faKhupzbZ0nib7Md4G-4c_eK5kFI9O3raMBX3XC-ydT7h2ehRw7kUFKNPab3BvkhC_IQoIyimqxdRUTNoFKXGwf1Kua2-qF0DbJ2TQf2kABQaUHW8BQQ9phdm4fTLIc2uI8OQm7HVOU4TQHPb02HKbuz6nEw8HsiG_RbBCA',
        'origin': 'https://www.plugshare.com',
        'referer': 'https://www.plugshare.com/',
        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mouse-House/7.4 (spider_monkey spider info at www.mobrien.com/sm.shtml)',
    }

    response = requests.get(
        'https://api.plugshare.com/v3/locations/region?access=1&cost=true&count=500&include_coming_soon=true&latitude=38.072884734128635&longitude=23.824059464598005&minimal=0&outlets=%5B%7B%22connector%22:6,%22power%22:1%7D,%7B%22connector%22:13,%22power%22:0%7D,%7B%22connector%22:3,%22power%22:0%7D,%7B%22connector%22:2,%22power%22:0%7D,%7B%22connector%22:6,%22power%22:0%7D,%7B%22connector%22:4,%22power%22:0%7D,%7B%22connector%22:7,%22power%22:0%7D,%7B%22connector%22:8,%22power%22:0%7D,%7B%22connector%22:14,%22power%22:0%7D,%7B%22connector%22:15,%22power%22:0%7D,%7B%22connector%22:10,%22power%22:0%7D,%7B%22connector%22:24,%22power%22:0%7D%5D&spanLat=7.441991587816389&spanLng=11.206298828125',
        headers=headers,
    )

    data = json.loads(response.content.decode('utf8'))

    return data

def plugShare():
    data = getPlugShare()
    data_list = []
    for station in data:
        name = station['name']
        lat = station['latitude']
        long = station['longitude']
        address = station['address']
        type = 'type 2'
        origin = 'PlugShare'
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