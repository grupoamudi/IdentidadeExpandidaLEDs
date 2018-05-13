byte brilho = 0; //variavel global para intensidade do brilho do led

void setup() {
  
Serial.begin(9600); //abre o serial
pinMode(3,OUTPUT);   //usa a porta 3 que tem PWM no Nano

}

void loop() {

  if (Serial.available() > 0) { // ve se a comunicacao esta disponivel
    brilho = Serial.parseInt();    // le e salva o valor de entrada
    analogWrite(3 , brilho);
  }

}
