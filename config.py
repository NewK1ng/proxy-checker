import os
from dotenv import load_dotenv

load_dotenv()

_COUNTRY_PROXY = os.getenv("COUNTRY_PROXY")
_REGION_PROXY = os.getenv("REGION_PROXY")
_CITY_PROXY = os.getenv("CITY_PROXY")


def get_city_proxy(country, city):
    return _CITY_PROXY.format(country=country, city=city)


def get_region_proxy(country, region):
    return _REGION_PROXY.format(country=country, state=region)


def get_country_proxy(country):
    return _COUNTRY_PROXY.format(country=country)