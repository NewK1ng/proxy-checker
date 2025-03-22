import requests

ip_list = []
ip_location_list = []
proxy_location_list = []
file_path_to_ips = "ip_list.txt"


def get_ip_list(file_path):
    with open(file_path, 'r') as file:
        ip_list = [line.strip() for line in file.readlines()]
        
    return ip_list


def get_ip_info(ip):
    url = f"https://ipinfo.io/{ip}"
    response = requests.get(url).json()
    
    return {
        "country": response["country"],
        "region": response["region"],
        "city": response["city"]
    } 

ip_list = get_ip_list(file_path_to_ips)
print(f"Total IPs: {len(ip_list)}")

for ip in ip_list:
    ip_info = get_ip_info(ip)
    ip_location_list.append(ip_info)

print(f"Received {len(ip_location_list)} IP locations")
print(ip_location_list)