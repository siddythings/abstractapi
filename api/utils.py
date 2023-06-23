import requests
from django.conf import settings

def get_geolocation_data(ip_address):
    url = f"https://ipgeolocation.abstractapi.com/v1/?api_key={settings.GEOLOCATION_ABSTRACT_API_KEY}&ip_address={ip_address}"
    response = requests.get(url)
    data = response.json()
    return data

def check_holiday(country_code, day, month, year):
    url = f"https://holidays.abstractapi.com/v1/?api_key={settings.HOLIDAY_ABSTRACT_API_KEY}&country={country_code}&year={year}&month={month}&day={day}"
    response = requests.get(url)
    data = response.json()
    holiday = ""
    if data:
        for obj in data:
            holiday += obj.get("name","") + ", "
    return holiday
