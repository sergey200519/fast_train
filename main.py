import requests
from  bs4 import BeautifulSoup
import json

def fun(item):
    try:
        url = item.find("a")["href"]
    except:
        return ""
    if "html" in str(url):
        temp = url.replace(".html", "")
        return temp.replace("http://3ty.ru/rasp/", "")
    if "gdevagon" in str(url):
        return url.replace("http://www.gdevagon.ru/scripts/info/station_detail.php?stid=", "")
    return url.replace("http://rasp.yandex.ru/info/station/", "")

def fun2(text):
    key = 0
    i = 0
    while i < len(text):
        if text[i].isupper():
            key = i
        i += 1
    return text[key:].strip()


url = "http://osm.sbin.ru/esr/region:mosobl:l"

req = requests.get(url)
src = req.text
soup = BeautifulSoup(src, "lxml")
table = soup.find("table")
tr = table.find_all("tr")
answer = {}
for item in tr:
    station = item.find_all("td")
    if len(station) <= 1:
        continue
    link = fun(station[-2])
    answer[fun2(station[1].text)] = link

with open("station.json", "a", encoding="utf-8") as f:
    json.dump(answer, f, indent=4, ensure_ascii=False)
print(answer)


#
