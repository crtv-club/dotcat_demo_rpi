#include <SPI.h>

#include <printf.h>
#include <RF24_config.h>
#include <nRF24L01.h>
#include <RF24.h>
#include <stdlib.h>

int msg[3];
RF24 radio(9,10);
const uint64_t pipe = 0xe7e7e7e7e7LL;
//int SW1 = 7;

void setup(void){
 Serial.begin(9600);
 printf_begin();
 
 radio.begin();
 
 radio.setRetries(15, 15);
 radio.setPayloadSize(4);
 radio.setChannel(0x4c);
 
 radio.setCRCLength(RF24_CRC_16);
 
 radio.setDataRate(RF24_1MBPS);
 radio.setPALevel(RF24_PA_MAX);
 radio.openWritingPipe(pipe);
}

void loop(void) {
 //if (digitalRead(SW1) == HIGH){
 msg[0] = rand();
 msg[1] = rand();
 msg[2] = rand();
 radio.write(msg, 3);
 delay(1);
 //}
}
