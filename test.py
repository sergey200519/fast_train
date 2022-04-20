import json
import requests
from bs4 import BeautifulSoup


json_file = ""
with open("station.json", "r") as f:
    json_file = json.loads(f.read())

stations = {}
i = 0
headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
}

for key, value in json_file.items():

    print(key.strip())
    url = f"https://wikislovo.ru/inflect/{key.strip().lower()}"


    try:
        req = requests.get(url)
        src = req.text
        soup = BeautifulSoup(src, "lxml")
        table = soup.find(class_="table-striped").find("tbody")
        tr = table.find_all("tr")
        temp = []
        for item in tr:
            td = item.find_all("td")
            temp.append(str(td[2].text).title())

        temp2 = str(temp).replace("[", "").replace("'", "")
        stations[temp2.replace("]", "")] = value


    except:
        stations[key] = value

print(stations)

with open("stations.json", "a", encoding="utf-8") as f:
    json.dump(stations, f, indent=4, ensure_ascii=False)






#
