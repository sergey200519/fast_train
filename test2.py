import json
import requests
from bs4 import BeautifulSoup



stations = {}


url = f"https://wikislovo.ru/inflect/курская"

req = requests.get(url)
src = req.text
soup = BeautifulSoup(src, "lxml")
table = soup.find(class_="table-striped").find("tbody")
tr = table.find_all("tr")
temp = []
for item in tr:
    td = item.find_all("td")
    temp.append(td[2].text)
    print(td)
print(temp)
