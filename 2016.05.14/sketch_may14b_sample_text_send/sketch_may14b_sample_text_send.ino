void setup(){
  Serial.begin(9600);//Инициирует последовательное соединение 
  //и задает скорость передачи данных в бит/c
}

  void loop()
  {
    Serial.println("test");
    delay(1000);
  };
