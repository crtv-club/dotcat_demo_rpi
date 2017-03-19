#!/usr/bin/python
# -*- coding: utf-8 -
# Subscriber - отслеживает все темы, связанные с сенсорами ("/sensors/#")
# Куда копать:
#  * http://www.hivemq.com/blog/mqtt-client-library-paho-python
#  * http://www.eclipse.org/paho/clients/python/docs/

import paho.mqtt.client as mqtt
import time
import datetime

import csv

csvfile = open('values.csv', 'w')
fieldnames = ['value', 'time']
writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

writer.writeheader()

print(datetime.datetime.now())


# Инициализируем объект-клиент
client_printer = mqtt.Client(client_id="temp_logger", clean_session=False, userdata=None, protocol=mqtt.MQTTv311)

# Устанавливаем last will - сообещние, которое публикуется при обрыве соединения
client_printer.will_set("/wills/", payload="Empty printer will", qos=0, retain=False)


# Фукнция, которая реагирует на полученные сообщения
def on_message(client: mqtt.Client, userdata, msg: mqtt.MQTTMessage):
    print(client)
    print(datetime.datetime.now())
    print(userdata)
    print(msg.payload)  # Данные в бинарном формате. Например b'from phone with love' или b'1478215437.172098'
    print(msg.topic)  # Тема сообщения, строка. Например "/sensors/phone"

    writer.writerow({'value': float(msg.payload), 'time': time.time()})

# Устанавливаем обработчик сообщений
client_printer.on_message = on_message

# Подключаемся к серверу
client_printer.connect("hostname_here")

# Подписываемся на все сенсоры
client_printer.subscribe("/sensors/temp/TEMP1")

# Запускаем вечный цикл работы с сетевым траффиком, обрываемый исключением
try:
    client_printer.loop_forever()

finally:  # Если выброшено исключение...
    print("disconnecting")
    client_printer.loop_stop()  # Останавливаем сетевой цикл, Иначе получим аварийный обрыв соединения
    # и брокер вышлет last will всем подписавшимся клиентам
    client_printer.disconnect()  # Отключаемся
    csvfile.close()
