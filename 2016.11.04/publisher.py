# Publisher - публикует информацию в тему /sensors/1
# Куда копать:
#  * http://www.hivemq.com/blog/mqtt-client-library-paho-python
#  * http://www.eclipse.org/paho/clients/python/docs/

import paho.mqtt.client as mqtt
import time

# Инициализируем объект-клиент
client_sensor = mqtt.Client(client_id="sensor", clean_session=False, userdata=None, protocol=mqtt.MQTTv311)

# Устанавливаем last will - сообещние, которое публикуется при обрыве соединения
client_sensor.will_set("/wills/", payload="Empty will", qos=0, retain=False)

# Подключаемся к серверу
client_sensor.connect("localhost")

# Запускаем цикл работы с сетевым траффиком
client_sensor.loop_start()

# Запускаем вечный цикл, обрываемый исключением
try:
    while True:
        # Публикуем текущее время, печатаем результат передачи номер сообщения в сессии
        print(client_sensor.publish("/sensors/1", payload=time.time(), qos=0, retain=False))

        # ...раз в 2 секунды
        time.sleep(2)
finally:  # Если выброшено исключение...
    print("disconnecting")
    client_sensor.loop_stop()  # Останавливаем сетевой цикл, Иначе получим аварийный обрыв соединения
    # и брокер вышлет last will всем подписавшимся клиентам
    client_sensor.disconnect()  # Отключаемся
