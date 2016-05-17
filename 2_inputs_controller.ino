/*
Materials are took from "Exploring Arduino"
*/

//LCD text with incrementing number
//Include the library code:

#include <LiquidCrystal.h>
#include <math.h>
//Start the time at 0
int time = 0;
//Initialize the library with the numbers of the interface pins
LiquidCrystal lcd(2, 3, 4, 5, 6, 7);

//Number of Light Sensors on analog pins
const uint8_t LIGHT0 = 0; //  Entrance to office
const uint8_t LIGHT1 = 1; //  Entrance to bedroom
const uint8_t LIGHT2 = 2; //  Exit from office
const uint8_t LIGHT3 = 3; //  Exit from bedroom
const uint8_t LIGHT4 = 4;
const uint8_t LIGHT5 = 5;

//variable to hold the analog reading
uint8_t value0 = 0; 
uint8_t value1 = 0;
uint8_t value2 = 0;
uint8_t value3 = 0;
uint8_t value4 = 0;
uint8_t value5 = 0;

uint8_t old_value0 = 0;
uint8_t old_value1 = 0;
uint8_t old_value2 = 0;
uint8_t old_value3 = 0;
uint8_t old_value4 = 0;
uint8_t old_value5 = 0;

typedef unsigned short int USHORT;
const uint8_t DIFFERENCE = 30;
const uint8_t THRESHOLD = 500;

char buf[4];


/*--------------------------------------------------------------------*/

// Variables for buttons

//  Buttons states
//  Current states:
boolean b1_current_state = LOW;
boolean b2_current_state = LOW;
boolean b3_current_state = LOW;
boolean b4_current_state = LOW;
boolean b5_current_state = LOW;
boolean b6_current_state = LOW;
//  Last states:
boolean b1_last_state = LOW;
boolean b2_last_state = LOW;
boolean b3_last_state = LOW;
boolean b4_last_state = LOW;
boolean b5_last_state = LOW;
boolean b6_last_state = LOW;
//  Buttons ports
const uint8_t b1 = 8;
const uint8_t b2 = 9;
const uint8_t b3 = 10;
const uint8_t b4 = 11;
const uint8_t b5 = 12;
const uint8_t b6 = 13;


char & GetBufByValue(const int & _val)
{
  if (_val < 1000 && _val > 99) {
    sprintf(buf, "0%d", _val);
  } else if (_val < 100 && _val > 9){
    sprintf(buf, "00%d", _val);
  } else if (_val < 10) {
    sprintf(buf, "000%d", _val);
  }
  return *buf;
}

void PrintLightValue(int _val)
{
  lcd.setCursor(11,0);
  *buf = GetBufByValue(_val);
  lcd.print(buf);
}

void PrintMessage(char * _msg)
{
  lcd.setCursor(0,1);
  if (sizeof(_msg) / sizeof(char*) > 16) {
    lcd.print("Error 1!");
  } else {
    lcd.print(_msg);
  }
}



void PrintByIndex(int _place, int _value)
{
  lcd.setCursor(_place * 5 % 15, (_place) / 3);
  *buf = GetBufByValue(_value);
  lcd.print(buf);
}


///////////////////////////////////////////////////////////


void setup()
{
  Serial.begin(9600);
  pinMode(b1, INPUT);
  pinMode(b2, INPUT);
  pinMode(b3, INPUT);
  pinMode(b4, INPUT);
  pinMode(b5, INPUT);
  pinMode(b6, INPUT);
  //Set up the LCD's number of columns and rows:
  lcd.begin(16, 2);
  //Print a message to the LCD.
  //lcd.print("ADC value: ");
  lcd.setCursor(0,0);
  lcd.print("---- ---- ----  ");
  lcd.setCursor(0,1);
  lcd.print("---- ---- ----  ");

  
}

boolean debounce(boolean _current, boolean _last, uint8_t _port) {
  boolean current = digitalRead(_port); //Read the button state
  if (_last != _current) {
    delay(5); //wait 5ms                          
    _current = digitalRead(_port); //read it again
  }
  return current; //return the current value
}

void loop()
{
  b1_current_state = debounce(b1_current_state, b1_last_state, b1);
  if (b1_last_state == LOW && b1_current_state == HIGH) {
    Serial.print("B1");
  }
  b1_last_state = b1_current_state;

  b2_current_state = debounce(b2_current_state, b2_last_state, b2);
  if (b2_last_state == LOW && b2_current_state == HIGH) {
    Serial.print("B2");
  }
  b2_last_state = b2_current_state;

  b3_current_state = debounce(b3_current_state, b3_last_state, b3);
  if (b3_last_state == LOW && b3_current_state == HIGH) {
    Serial.print("B3");
  }
  b3_last_state = b3_current_state;

  b4_current_state = debounce(b4_current_state, b4_last_state, b4);
  if (b4_last_state == LOW && b4_current_state == HIGH) {
    Serial.print("B4");
  }
  b4_last_state = b4_current_state;

  b5_current_state = debounce(b5_current_state, b5_last_state, b5);
  if (b5_last_state == LOW && b5_current_state == HIGH) {
    Serial.print("B5");
  }
  b5_last_state = b5_current_state;

  b6_current_state = debounce(b6_current_state, b6_last_state, b6);
  if (b6_last_state == LOW && b6_current_state == HIGH) {
    Serial.print("B6");
  }
  b6_last_state = b6_current_state;

  /*-------------------------------------------------------------------*/
  
  value0 = analogRead(LIGHT0);
  value1 = analogRead(LIGHT1);
  value2 = analogRead(LIGHT2);
  value3 = analogRead(LIGHT3);
  value4 = analogRead(LIGHT4);
  value5 = analogRead(LIGHT5);
  
  if (abs(value0 - old_value0) > DIFFERENCE) {
    if (value0 < THRESHOLD) {
      PrintByIndex(0, 1);
    } else {
      PrintByIndex(0, 0);
    }
  }
  if (abs(value1 - old_value1) > DIFFERENCE) {
    if (value1 < THRESHOLD) {
      PrintByIndex(1, 1);
    } else {
      PrintByIndex(1, 0);
    }
  }
  if (abs(value2 - old_value2) > DIFFERENCE) {
    if (value2 < THRESHOLD) {
      PrintByIndex(2, 1);
    } else {
      PrintByIndex(2, 0);
    }
  }
  if (abs(value3 - old_value3) > DIFFERENCE) {
    if (value3 < THRESHOLD) {
      PrintByIndex(3, 1);
    } else {
      PrintByIndex(3, 0);
    }
  }
  if (abs(value4 - old_value4) > DIFFERENCE) {
    if (value4 < THRESHOLD) {
      PrintByIndex(4, 1);
    } else {
      PrintByIndex(4, 0);
    }
  }
  if (abs(value5 - old_value5) > DIFFERENCE) {
    if (value5 < THRESHOLD) {
      PrintByIndex(5, 1);
    } else {
      PrintByIndex(5, 0);
    }
  }
  
  old_value0 = value0;
  old_value1 = value1;
  old_value2 = value2;
  old_value3 = value3;
  old_value4 = value4;
  old_value5 = value5;
  
  delay(100);
}
