unsigned const int SizeColum = 3;
unsigned const int SizeRows = 4;

char keymap[SizeColum][SizeRows] = {
  {'LED1', 'LED2', 'LED3', 'LED4'},
  {'LED5', 'LED6', 'LED7', 'LED8'},
  {'LED9', 'LED10', 'LED11', 'LED12'}
  };
 
const char noKey = 'n';
byte colums[SizeColum] = {1, 2, 3, }; //fix name of the pins
byte rows[SizeRows] = {4, 5, 6, 7};//fix name of the pins
unsigned int lastReadTime;
unsigned int bounseTime = 30;//ms
char CurrentKeyForSend = 'n';
void setup(){
  Serial.begin(11500);//Инициирует последовательное соединение 
  //и задает скорость передачи данных в бит/c
  lastReadTime = millis();//функция millis  выводит количество миллисекунд с 
  //момента начала выполнения программы. Дале записываем в временнную переменную
  for(int j = 0; j < SizeColum; j++){
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
      Serial.print(key);
      CurrentKeyForSend = key;
    };
    delay (50);
  };
  
  char getKeyPress(){
    char foundKey = noKey;
    if((millis() - lastReadTime) > bounseTime)
    {//Если время с начала работы программы минус
      //последнее считаннове время больше 30мс(bounceTime)
      for(int c = 0; c < SizeColum; c++)
      {//подаем сигнал на вертикальные дорожки
        pinMode(colums[c], OUTPUT);
        digitalWrite(colums[c], LOW);
        //опрашиваем горизонтальные дорожки 
        for(int r = 0; r < SizeRows; r++)
        {
          if(digitalRead((rows[r])) == LOW)
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
  };
  char CurrentKey()
  {
    return CurrentKeyForSend;
  }
  
   
   
