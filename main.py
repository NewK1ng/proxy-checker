import httpx
import time
import json
from config import get_city_proxy, get_region_proxy, get_country_proxy

ip_list = []
ip_location_list = []
proxy_location_list = []
file_path_to_ips = "ip_list.txt"


def make_proxy(country = None, region = None, city = None):
    if city:
        city = city.replace("saint", "st")
        city = city.replace(" ", "")
        proxy = f'socks5h://{get_city_proxy(country, city)}'
    elif region:
        region = region.replace(" ", "")
        proxy = f'socks5h://{get_region_proxy(country, region)}'
    else:
        proxy = f'socks5h://{get_country_proxy(country)}'            
    
    print(proxy)
    return proxy
    

def get_ip_list(file_path):
    with open(file_path, 'r') as file:
        ip_list = [line.strip() for line in file.readlines()]
        
    return ip_list


def get_proxy_ip(country, region, city):
    
    url = "https://ipinfo.io"
    response = None
    
    for i in range(3):
        try:
            if i == 0:
                with httpx.Client(proxy=make_proxy(country=country, city=city)) as client:
                    response = client.get(url, timeout=10).json()
                    break 
            if i == 1:
                with httpx.Client(proxy=make_proxy(country=country,region=region)) as client:
                    response = client.get(url, timeout=10).json()
                    break 
            if i == 2:
                with httpx.Client(proxy=make_proxy(country=country)) as client:
                    response = client.get(url, timeout=10).json()
                    break                     
        except httpx.ProxyError:
            continue
        except httpx.ConnectTimeout:
            continue
        except json.decoder.JSONDecodeError:
            continue
    
    return {
        "country": response.get("country", "bad").lower(),
        "region": response.get("region", "bad").lower(),
        "city": response.get("city", "bad").lower()
    }     


def get_ip_info(ip):
    
    url = f"https://ipinfo.io/{ip}"
    with httpx.Client() as client:
        response = client.get(url, timeout=5).json()
    
    return {
        "country": response.get("country", "unknown").lower(),
        "region": response.get("region", "unknown").lower(),
        "city": response.get("city", "unknown").lower()
    } 


ip_list = get_ip_list(file_path_to_ips)

i = 0

for ip in ip_list:
    ip_info = get_ip_info(ip)
    ip_location_list.append(ip_info)
    time.sleep(2)
    proxy_ip_info = get_proxy_ip(country=ip_info["country"], region=ip_info["region"],city=ip_info["city"])
    proxy_location_list.append(proxy_ip_info)
    i += 1
    print(i)
    
    
def compare_locations(ip_list, proxy_list):
    full_match = 0
    country_region_match = 0
    country_match = 0

    for ip_info, proxy_info in zip(ip_list, proxy_list):
        if ip_info == proxy_info:
            full_match += 1  # Exact match on all three fields
        elif ip_info["country"] == proxy_info["country"] and ip_info["region"] == proxy_info["region"]:
            country_region_match += 1  # Match on country & region
        elif ip_info["country"] == proxy_info["country"]:
            country_match += 1  # Match on country only

    return full_match, country_region_match, country_match    

print(f"Received {len(ip_location_list)} IP locations")
print(f"Received {len(ip_location_list)} PROXY IP locations\n")

full, country_region, country = compare_locations(ip_location_list, proxy_location_list)

print("COUNTRY MATCH:", country)
print("COUNTRY-REGION MATCH:", country_region)
print("SAME LOCATIONS:", full)
