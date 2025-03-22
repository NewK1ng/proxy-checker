import os
from dotenv import load_dotenv

load_dotenv()

_USERNAME_COUNTRY = os.getenv("USERNAME_COUNTRY")
_USERNAME_STATE = os.getenv("USERNAME_STATE")
_USERNAME_CITY = os.getenv("USERNAME_CITY")
PASSWORD = os.getenv("PASSWORD")
IP = os.getenv("IP")
PORT = os.getenv("PORT")

def get_username_country(country):
    return _USERNAME_COUNTRY.format(country=country)

def get_username_state(country, state):
    return _USERNAME_STATE.format(country=country, state=state)

def get_username_city(country, city):
    return _USERNAME_CITY.format(country=country, city=city)