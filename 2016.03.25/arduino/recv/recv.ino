#include <SPI.h>

#include <printf.h>
#include <RF24_config.h>
#include <nRF24L01.h>
#include <RF24.h>

int msg[1];
RF24 radio(9,10);
const uint64_t pipe = 0xc2c2c2c2c2LL;

void setup(void){
 Serial.begin(9600);
 printf_begin();
 
 radio.begin();
 
 radio.setRetries(15, 15);
 radio.setPayloadSize(8);
 radio.setChannel(0x4c);
 
 radio.setCRCLength(RF24_CRC_16);
 
 radio.setDataRate(RF24_1MBPS);
 radio.setPALevel(RF24_PA_MAX);

 radio.openReadingPipe(1,pipe);
 radio.startListening();
}

void loop(void) {
 if (radio.available()) {
   radio.read(msg, 1);      
   Serial.println(msg[0]);
 }
 else {
   Serial.println("No radio available");
   radio.printDetails();
 }
   
  delay(1000);
}
