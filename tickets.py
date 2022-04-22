import requests
import json
import datetime

class Request:
    def __init__(self, url):
        self.url = url

    def get(self, params):
        src = requests.get(self.url, params=params)
        with open("log.json", "a", encoding="utf-8") as f:
            json.dump(json.loads(src.text), f, indent=4, ensure_ascii=False)
        answer = json.loads(src.text)
        try:
            if answer["error"]["http_code"] != 200 or answer["error"]["http_code"] != "200":
                return False
        except:
            return answer

class Tickets:
    not_found_station = False

    def __init__(self, api_key, a, b, datetime=str(datetime.date.today()), limit="1000", url="https://api.rasp.yandex.net/v3.0/search/"):
        self.api_key = api_key
        self.a = a
        self.b = b
        self.date = datetime
        self.limit = limit
        self.url = url

    def simplify(self, full_json):
        tickets = {}
        n = int(full_json["pagination"]["total"])
        full_tickets = full_json["segments"]
        i = 0
        while i < n:
            ticket = full_tickets[i]
            if ticket["tickets_info"] == None:
                i += 1
                continue
            try:
                price = ticket["tickets_info"]["places"][0]["price"]["whole"]
            except:
                price = None
            info = {
                "title": ticket["thread"]["title"],
                "from": ticket["from"]["title"],
                "to": ticket["to"]["title"],
                "price": price

            }
            tickets[ticket["arrival"]] = info
            i += 1
        return tickets


    def tickets(self):
        self.__validate()
        codes = self.search()
        if self.not_found_station:
            return "Станция не найдена"
        params = self.collecting_data_for_request(codes)
        req = Request(self.url).get(params)
        if not req:
            return "Не удалось найти билет"
        answer = self.simplify(req)
        try:
            with open("answer.json", "a", encoding="utf-8") as f:
                json.dump(answer, f, indent=4, ensure_ascii=False)
        except:
            print("error save json")
        return answer

    def collecting_data_for_request(self, codes):
        params = {
                "apikey": self.api_key,
                "from": f"{codes['a_code']['type']}{codes['a_code']['value']}",
                "to": f"{codes['b_code']['type']}{codes['b_code']['value']}",
                "format": "json",
                "date": self.date,
                "transport_types": "suburban",
                "show_systems": "yandex",
                "direction": "all",
                "limit": self.limit
            }
        return params

    def __validate(self):
        self.a = self.a.title()
        self.b = self.b.title()

    def type_code(self, code):
        if len(code) == 7:
            return "s"
        else:
            return "c"

    def search(self):
        a_code = ""
        b_code = ""
        with open("stations.json", "r") as f:
            stations = dict(json.loads(f.read()))

        for key, value in stations.items():
            if self.a in key:
                a_code = value
            if self.b in key:
                b_code = value
        if a_code == "" or b_code == "":
            self.not_found_station = True
        return {
                "a_code": {"value": a_code,
                            "type": self.type_code(a_code)},
                "b_code": {"value": b_code,
                            "type": self.type_code(b_code)}
                }















if __name__ == "__main__":
    key =  "a56d14a1-cf2c-4f98-b770-fc67c0537074"
    a = Tickets(key, "Моссельмаш", "Разумовская")
    b = a.tickets()

    # print(str(datetime.date.today())



#
