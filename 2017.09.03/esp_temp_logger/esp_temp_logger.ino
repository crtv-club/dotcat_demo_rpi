#include <OneWire.h>
#include <DallasTemperature.h>

#include <ESP8266WiFi.h>
#include <PubSubClient.h>

// Include connection settings file (don't forget to edit it)
#include "connection_settings.h"

// Declare a number of pin that is used for OneWire communtication
#define ONE_WIRE_PIN 13

// Initialize an object for OneWire communication
OneWire oneWireBus(ONE_WIRE_PIN);

// Initialize a controller object for Dallas thermometers
DallasTemperature tempSensors(&oneWireBus);

// Define baudrate of serial interface exactly in one place
#define SERIAL_SPEED 115200

// Define deep sleep interval in microseconds (1 second = 1 000 000 us = 1e6 us)
#define DEEP_SLEEP_INTERVAL_US 360e6

// Define another magic number - a delay between commands on OneWire
#define SMALL_DELAY 10

// Initialize WiFi client and corresponding MQTT client
WiFiClient wifiClient;
const String hostname = String(MQTT_BROKER_HOSTNAME);
PubSubClient mqttClient(wifiClient);

void setup() {
  // put your setup code here, to run once:

  // Setup serial interface
  Serial.begin(SERIAL_SPEED);

  // Send greeting message
  Serial.println(); // Print empty line after startup garbage (e.g. own startup messages of ESP8266)
  Serial.println("Starting up...");

  // Begin communication with sensors
  tempSensors.begin();

  connectWiFi();
  mqttClient.setServer(MQTT_BROKER_HOSTNAME, MQTT_BROKER_PORT);

  Serial.println("Start up finished");
}

void connectWiFi() {
  // Initialize temporary variables that are needed for static IP setup
  const IPAddress staticIP(WIFI_IP);
  const IPAddress gateway(WIFI_GATEWAY);
  const IPAddress subnet(WIFI_SUBNET);

  // Initialize static IP configuration
  WiFi.config(staticIP, gateway, subnet);

  // Begin WiFi connection procedure
  Serial.print("Connecting to ");
  Serial.print(WIFI_SSID);
  Serial.print(" access point");
  
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  // Wait until connected:
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }

  // Print result
  Serial.println();
  Serial.println("Connected");
}

void loop() {
  // put your main code here, to run repeatedly:

  // Actually, this loop will be executed only once :).
  
  // On the end of iteration 'ESP.deep_sleep' will be called and MCU fill be halted until rebooted,
  // by internal RTC or by external reset signal ('low' pulse with duration > 100 us).

  sensorRoutine();

  // delay(10000); // Debug: sleep for 10 seconds to measure current consumption

  Serial.println("Going to sleep...");

  // Go to sleep and skip radio calibration on wakeup
  ESP.deepSleep(DEEP_SLEEP_INTERVAL_US, WAKE_NO_RFCAL);
}

void sensorRoutine() {
  // Fetch data from the first sensor and send it to MQTT broker

  // Try to get temperature data from the first sensor
  float temperature;
  bool data_read = getFirstSensorData(&temperature);

  if (! data_read) {
    Serial.println("Temperature sensor is disconnected, no data retrieved");
    return;
  }

  Serial.print("Read temperature: ");
  Serial.print(temperature);
  Serial.println("°C");

  sendSensorData(temperature);
}

bool getFirstSensorData(float* _pData) {
  // Just a function which reads data from the first temperature sensor and saves it by _pData pointer
  // in a case of success.
  
  // Returns true if data was retrieved, false otherwise.

  // Check if any sensors connected
  uint8_t sensors_connected = tempSensors.getDeviceCount();

  if (! sensors_connected) {
    // Temperature sensor is disconnected, no data retrieved
    return false;
  }

  // Temperature MUST be requested before it can be read
  // requestTemperaturesByIndex() works unstable for some reason and likes to return +85 degrees of Celsius
  tempSensors.requestTemperatures();

  // Get temperature from the first sensor. It works fine but is slow
  *(_pData) = tempSensors.getTempCByIndex(0);

  // If the ID of sensor is already known, then it's better to send a direct request:
  // *(_pData) = tempSensors.getTempC(TEMP_SENSOR_ID);

  return true;
}

void sendSensorData(float temperature) {
  // Send fetched data to broker with predefined topic

  Serial.println("Connecting to broker and sending data...");

  #define BUFFER_SIZE 13

  char buffer[BUFFER_SIZE]; // The longest line is ID. It looks like "ESP 7FFFFFFF"

  snprintf(buffer, BUFFER_SIZE, "ESP %x", ESP.getChipId()); // Generate string containing ID of client

  // Establish connection to MQTT broker
  while (! mqttClient.connected()) {
    if (mqttClient.connect(buffer)) {
      break;
    }
    else {
      Serial.print(".");
      delay(500);
    }
  }

  // Convert temperature data to sting in format "0.10" or "11.66"
  dtostrf(temperature, 1, 2, buffer);

  // Publish temperature string to MQTT broker and then disconnect gracefully
  mqttClient.publish(MQTT_PUB_TOPIC, buffer);
  mqttClient.disconnect();
}

