#include <OneWire.h>
#include <DallasTemperature.h>

// Declare a number of pin that is used for OneWire communtication
#define ONE_WIRE_PIN 13

// Initialize an object for OneWire communication
OneWire oneWireBus(ONE_WIRE_PIN);

// Initialize a controller object for Dallas thermometers
DallasTemperature tempSensors(&oneWireBus);

// Define baudrate of serial interface exactly in one place
#define SERIAL_SPEED 115200

// Define deep sleep interval in microseconds (1 second = 1 000 000 us = 1e6 us)
#define DEEP_SLEEP_INTERVAL_US 5e6

// Define another magic number - a delay between commands on OneWire
#define SMALL_DELAY 10

void setup() {
  // put your setup code here, to run once:

  // Setup serial interface
  Serial.begin(SERIAL_SPEED);

  // Send greeting message
  Serial.println(); // Print empty line after startup garbage (e.g. own startup messages of ESP8266)
  Serial.println("Startup finished");

  // Begin communication with sensors
  tempSensors.begin();

  // Small delay to finish discovery of devices
  delay(SMALL_DELAY);
}

void loop() {
  // put your main code here, to run repeatedly:

  // Actually, this loop will be executed only once :).
  
  // On the end of iteration 'ESP.deep_sleep' will be called and MCU fill be halted until rebooted,
  // by internal RTC or by external reset signal ('low' pulse with duration > 100 us).

  printSensorData();

  Serial.println("Going to sleep...");

  // delay(10000); // Debug: sleep for 10 seconds to measure current consumption

  // Go to sleep and disable WiFi on wakeup
  ESP.deepSleep(DEEP_SLEEP_INTERVAL_US, WAKE_RF_DISABLED);
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

void printSensorData() {
  // Just a function which reads data from the first temperature sensor
  // and prints it to serial console.

  float temperature;
  bool data_read = getFirstSensorData(&temperature);

  if (! data_read) {
    Serial.println("Temperature sensor is disconnected, no data retrieved");
    return;
  }

  Serial.print("Read temperature: ");
  Serial.print(temperature);
  Serial.println("°C");
}

