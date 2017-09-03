// Replace dots with your connection params

#define WIFI_SSID "....."
#define WIFI_PASSWORD "....."

// Static IP settings
#define WIFI_IP 192,168,1,144
#define WIFI_GATEWAY 192,168,1,1
#define WIFI_SUBNET 255,255,255,0

// Settings of ThingSpeak service just for example:
#define MQTT_BROKER_HOSTNAME "mqtt.thingspeak.com"
#define MQTT_BROKER_PORT 1883
#define MQTT_PUB_TOPIC "channels/<channelID>/publish/fields/field<fieldnumber>/<apikey>"
