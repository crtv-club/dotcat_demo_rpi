/*
 Basic ESP8266 MQTT example

 This sketch demonstrates the capabilities of the pubsub library in combination
 with the ESP8266 board/library.

 It connects to an MQTT server then:
  - publishes current temperature in Celsius to the topic "pubTopic" every two seconds

 It will reconnect to the server if the connection is lost using a blocking
 reconnect function. See the 'mqtt_reconnect_nonblocking' example for how to
 achieve the same result without blocking the main loop.

 To install the ESP8266 board, (using Arduino 1.6.4+):
  - Add the following 3rd party board manager under "File -> Preferences -> Additional Boards Manager URLs":
       http://arduino.esp8266.com/stable/package_esp8266com_index.json
  - Open the "Tools -> Board -> Board Manager" and click install for the ESP8266"
  - Select your ESP8266 in "Tools -> Board"

*/

// OneWire DS18S20, DS18B20, DS1822 Temperature Example
//
// http://www.pjrc.com/teensy/td_libs_OneWire.html
//
// The DallasTemperature library can do all this work for you!
// http://milesburton.com/Dallas_Temperature_Control_Library


#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <OneWire.h>
#include <DallasTemperature.h>

#include "connection_settings.h"

#define ONE_HOUR_IN_MS 3600000
#define TEN_MINUTES_IN_MS 600000

WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = -TEN_MINUTES_IN_MS;
char msg[50];
const char* pubTopic = "/sensors/temp/TEMP1";

OneWire  oneWireBus(13);  // on pin 13 (a 4.7K resistor is necessary)
DallasTemperature sensors(&oneWireBus);

void setup_wifi() {
  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  randomSeed(micros());

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Create a random client ID
    String clientId = "ESP8266Client-";
    clientId += String(random(0xffff), HEX);
    // Attempt to connect
    if (client.connect(clientId.c_str())) {
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(9600);
  setup_wifi();
  client.setServer(mqtt_server, mqtt_port);
}

bool init_temp_sensors() {
  const int sensor_count = sensors.getDeviceCount();

  sensors.begin();

  if (sensor_count == 0) {
    Serial.println("No sensors connected");
  }
  else {
    Serial.print("Detected sensor count: ");
    Serial.println(sensor_count);
  }

  return sensor_count;
}

double read_temperature(int index_of_sensor) {
  sensors.requestTemperatures();
  const double temperature = sensors.getTempCByIndex(INDEX_OF_SENSOR);
  
  Serial.print("Temperature for Device ");
  Serial.print(INDEX_OF_SENSOR);
  Serial.print(" is: ");
  Serial.print(temperature);

  return temperature;
}

void publish_if_time_came(double temperature) {
  long now = millis();
  if (now - lastMsg > TEN_MINUTES_IN_MS) {
    lastMsg = now;
    dtostrf(temperature, 1, 2, msg);
    Serial.print("Publish message: ");
    Serial.println(msg);
    client.publish(pubTopic, msg, true);
  }
}

void loop_body() {
  #define INDEX_OF_SENSOR 0

  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  int count_sensors_connected = init_temp_sensors();

  if (! count_sensors_connected) {
    return;
  }

  if (count_sensors_connected <= INDEX_OF_SENSOR) {
    Serial.print("sensor number ");
    Serial.print(INDEX_OF_SENSOR);
    Serial.println(" is unavailable");

    return;
  }

  double temperature = read_temperature();
  
  publish_if_time_came(temperature);
}

void loop() {
  loop_body();
  delay(1000);
}

