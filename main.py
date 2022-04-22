from tickets import Tickets

A = input("Пункт A: ")
B = input("Пункт B: ")

key =  "a56d14a1-cf2c-4f98-b770-fc67c0537074"
tickets = Tickets(key, A, B, datetime="2022-04-22").tickets()
print(tickets)























#
