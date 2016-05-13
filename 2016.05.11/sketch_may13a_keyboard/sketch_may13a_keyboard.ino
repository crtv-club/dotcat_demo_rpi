unsigned const int SizeColumns = 3;
unsigned const int SizeRows = 4;

char keymap[SizeRows][SizeColumns] = {
  {'1', '2', '3'},
  {'4', '5', '6'},
  {'7', '8', '9'},
  {'*', '0', '#'} 
  };
 
const char noKey = 'n';
byte colums[SizeColumns] = { 2, 3, 4 }; //fix name of the pins
byte rows[SizeRows] = {5, 6, 7, 8};//fix name of the pins
unsigned int lastReadTime;
unsigned int bounceTime = 30;//ms
char CurrentKeyForSend = 'n';

const unsigned short int delay_key_press = 50;

char OldKey;
unsigned short int adCounter = 0;
const unsigned short int delay_cycle_time = 500; // ms

void setup(){
  Serial.begin(9600);//Инициирует последовательное соединение 
  //и задает скорость передачи данных в бит/c
  lastReadTime = millis();//функция millis  выводит количество миллисекунд с 
  //момента начала выполнения программы. Дале записываем в временнную переменную
  for(int j = 0; j < SizeColumns; j++){
    pinMode(colums[j],INPUT);//устанавливаем пины на ввод
  };
  
   for (int i = 0; i < SizeRows; i++){
    pinMode(rows[i], INPUT);//устанавливаем пины на ввод
    digitalWrite(rows[i], HIGH);//устанавливаем значение 1
  };
}
  void loop()
  {
    char key = getKeyPress();
    if(key != noKey)
    {
      PrintKey(key);
      CurrentKeyForSend = key;
    };
    delay (delay_key_press);
  };
  
char getKeyPress(){
  char foundKey = noKey;
  if ( (millis() - lastReadTime) > bounceTime ) {
    //Если время с начала работы программы минус
    //последнее считаннове время больше 30мс(bounceTime)
    for(int c = 0; c < SizeColumns; c++)
    {//подаем сигнал на вертикальные дорожки
      pinMode(colums[c], OUTPUT);
      digitalWrite(colums[c], LOW);
      //опрашиваем горизонтальные дорожки 
      for(int r = 0; r < SizeRows; r++)
      {
        if(digitalRead(rows[r]) == LOW)
        {//если у нас на горизонтальной дорожке
          //будет значение 0 то запоминаем позиию
          foundKey = keymap[r][c];
          
        };
      };
      digitalWrite(colums[c], HIGH);
      pinMode(colums[c], INPUT);
      if(foundKey != noKey)
      {
        break;
      };
    };
    lastReadTime = millis();
  };
  return foundKey;
}

void PrintKey(char const _key) {
  if ( _key == OldKey ) {
      if ( adCounter < ( delay_cycle_time / delay_key_press ) ) {
          ++adCounter;
      }
      else {
          Serial.println(_key);
      }
  }
  else {
      Serial.println(_key);
      OldKey = _key;
      adCounter = 0;
  }
}

char CurrentKey()
{
  return CurrentKeyForSend;
}
  
   
   

