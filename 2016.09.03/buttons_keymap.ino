
unsigned const int SizeColumns = 2;
unsigned const int SizeRows = 3;



const char noKey = 'n';
byte colums[SizeColumns] = { 2, 3 }; //fix name of the pins
byte rows[SizeRows] = { 4, 5, 6 };//fix name of the pins

//  Antibounce system variables
unsigned int lastReadTime;
unsigned int bounceTime = 30;//ms

const unsigned short int delay_key_press = 50;

//-------------------------------------------------------------------

//  Messages to send
char keymap[SizeRows][SizeColumns] = {
  { 'B1', 'B2' },
  { 'B3', 'B4' },
  { 'B5', 'B6' }
};

//  Current button states
boolean current_state[SizeRows][SizeColumns] = {
  { LOW, LOW },
  { LOW, LOW },
  { LOW, LOW }
};

//  Last button states
boolean last_state[SizeRows][SizeColumns] = {
  { LOW, LOW },
  { LOW, LOW },
  { LOW, LOW }
};


//-------------------------------------------------------------------



void setup(){
  
  Serial.begin(9600);
  
  lastReadTime = millis();
  
  for(int j = 0; j < SizeColumns; j++){
    pinMode(colums[j],INPUT); // Setting pins for input
  };
  
  for (int i = 0; i < SizeRows; i++){
    pinMode(rows[i], INPUT); // Setting pins for input
    digitalWrite(rows[i], HIGH);
  };
}


void loop() {
  char foundKey = noKey;
  if ( (millis() - lastReadTime) > bounceTime ) {
    
    //Если время с начала работы программы минус
    //последнее считаннове время больше 30мс(bounceTime)
    
    for(int c = 0; c < SizeColumns; c++)
    {
      //подаем сигнал на вертикальные дорожки
      pinMode(colums[c], OUTPUT);
      digitalWrite(colums[c], LOW);
      //опрашиваем горизонтальные дорожки 
      for(int r = 0; r < SizeRows; r++)
      {
        if(digitalRead(rows[r]) == LOW)
        {
          //если у нас на горизонтальной дорожке
          //будет значение 0 то запоминаем позиию
          foundKey = keymap[r][c];
          // И отправляем её в Serial
          
        }
      }
      
      digitalWrite(colums[c], HIGH);
      pinMode(colums[c], INPUT);
      
      if(foundKey != noKey)
      {
        break;
      }
    }
    lastReadTime = millis();
  }
}
