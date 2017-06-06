# CPU Temp Publisher - публикует информацию о температуре процессора
# в тему /sensors/book1/cpu0

# Куда копать:
#  * http://www.hivemq.com/blog/mqtt-client-library-paho-python
#  * http://www.eclipse.org/paho/clients/python/docs/
#  * https://github.com/paroj/sensors.py/blob/master/example.py

import paho.mqtt.client as mqtt
import sensors
import time

# Инициализируем объект-клиент
client_sensor = mqtt.Client(client_id="BookPublisher", clean_session=False, userdata=None, protocol=mqtt.MQTTv311)

# Подключаемся к серверу
client_sensor.connect("ks-cube.tk")

# Запускаем цикл работы с сетевым траффиком
client_sensor.loop_start()

# Запускаем вечный цикл, обрываемый исключением
try:
    sensors.init()

    # Получаем объект для считвания значения температуры
    chip, nr = sensors.get_detected_chips(sensors.parse_chip_name("dell_smm-virtual-0"), 0)

    while True:
        # Получаем текущую температуру 2-го эелемента чипа dell_smm-virtual-0 (CPU)
        payload = sensors.get_value(chip, 2)

        # Публикуем текущую температура, печатаем результат передачи номер сообщения в сессии
        print("temp: {0}".format(payload))
        print(client_sensor.publish("/sensors/book1/cpu", payload=payload, qos=0, retain=False))

        # ...раз в 10 секунд
        time.sleep(10)
finally:  # Если выброшено исключение...
    print("disconnecting")
    client_sensor.loop_stop()  # Останавливаем сетевой цикл, Иначе получим аварийный обрыв соединения
    # и брокер вышлет last will всем подписавшимся клиентам
    client_sensor.disconnect()  # Отключаемся

    sensors.cleanup()  # Чистим после себя
