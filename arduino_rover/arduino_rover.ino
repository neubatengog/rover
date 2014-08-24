#include <Servo.h>
 
 
#define MOTOR1A 4      //L1
#define MOTOR1B 3     // L2
#define MOTOR1_VELO 2 // EA
 
#define MOTOR2A 7     // L3
#define MOTOR2B 6     // L4
#define MOTOR2_VELO 5 // EB
   
   
#define SERIALSPEED 57600
 
#define SERVOCAMARA 13
 
Servo camara;
 
int ByteEntrada = 0;       // datos de entrada 
boolean stringCompleto = false;  // cunado se ha completado el string
 
int velocidad_val = 255;
 
int sw = 0;
int pos = 90;
 
void setup()
{ 
  //motor 1  
  pinMode(MOTOR1A,OUTPUT);  
  pinMode(MOTOR1B,OUTPUT);  
  pinMode(MOTOR1_VELO,OUTPUT);     
  //motor 2  
  pinMode(MOTOR2A,OUTPUT);
  pinMode(MOTOR2B,OUTPUT);   
  pinMode(MOTOR2_VELO,OUTPUT);      
  //serial
  Serial.begin(SERIALSPEED);
    //servo camara
  camara.attach(SERVOCAMARA);	
  Serial.println("<<<<ROVER 0.0000000001a>>>>");
  delay(1);
   
  

} 
 
//================Movimiento de servo de camara===============//
void izqCam()
{       
        pos = ((pos-5)<=0)?0:pos -=5;    
	camara.write(pos);
        delay(10);
	
}
 
void centrarCam()
{ 
	pos = 90;
	camara.write(pos);
        //Serial.println("Posicion:90");
	
}
 
void derCam( )
{ 
        pos = ((pos+5)>=180)?180:pos += 5;  
	camara.write(pos);
        //Serial.print("Posicion:");
        //Serial.println(pos);
        delay(10);
	
}
 
void paneo(){
        for(int a=90 ; a<=180; a++){
          camara.write(a);
          delay(10);
        }
        for(int a=180 ; a>=0; a--){
          camara.write(a);
          delay(10);
        }
        for(int a=0 ; a<=90; a++){
          camara.write(a);
          delay(10);
        }
        pos=90;
        Serial.println("<<Camara centrada>>");
        
}
 
//==============fin de movimineto de camara===================//
 
//=============Inicio movimineto de motores==================//
 
void parar(int motor)  
{  
   setVelocidad(motor, 0); 
   delay(1); 
  
} 
 
void parar_total()
{
  sw=0;
  parar(MOTOR1_VELO);
  parar(MOTOR2_VELO);
  //Serial.println("<<PARAR MOTORES>>");
}
  
void setVelocidad(int motor, int velocidad)  
{  
   if (motor == MOTOR1_VELO)  
      analogWrite(MOTOR1_VELO, velocidad);      
   else  
      analogWrite(MOTOR2_VELO, velocidad);
   delay(1); 
  
   //Serial.print("Velocidad actual:");
   //Serial.println(velocidad_val);    
}  
  
void atras()
{
    sw=1;
    digitalWrite(MOTOR1A,LOW);
    digitalWrite(MOTOR1B,HIGH); 
    
    digitalWrite(MOTOR2A,LOW);  
    digitalWrite(MOTOR2B,HIGH); 
    setVelocidad(MOTOR1_VELO, velocidad_val);
    setVelocidad(MOTOR2_VELO, velocidad_val);
    //Serial.println("ATRAS");
 
}
 
void adelante()
{
    digitalWrite(MOTOR1A,HIGH);  
    digitalWrite(MOTOR1B,LOW);  
    
    digitalWrite(MOTOR2A,HIGH);  
    digitalWrite(MOTOR2B,LOW);  
    
    setVelocidad(MOTOR1_VELO, velocidad_val);
    setVelocidad(MOTOR2_VELO, velocidad_val);
    //Serial.println("ADELANTE");
}  
 
void izq()
{
 
    digitalWrite(MOTOR1A,LOW);  
    digitalWrite(MOTOR1B,HIGH); 
    
    digitalWrite(MOTOR2A,HIGH);  
    digitalWrite(MOTOR2B,LOW);  
    
    setVelocidad(MOTOR1_VELO, 180);
    setVelocidad(MOTOR2_VELO, 160);
    //Serial.println("IZQ");
}  
 
void der()
{
   
    digitalWrite(MOTOR1A,HIGH); 
    digitalWrite(MOTOR1B,LOW); 
    
    digitalWrite(MOTOR2A,LOW); 
    digitalWrite(MOTOR2B,HIGH); 
    
    setVelocidad(MOTOR1_VELO, 160);
    setVelocidad(MOTOR2_VELO, 180);
    //Serial.println("DER");
}  
 
//=======================Fin moviento de motores====================//
 
 
 
void loop()
{ 
    if (Serial.available() > 0)
    {
      ByteEntrada = Serial.read();
      delay(1); 
      if (ByteEntrada == 106) //j
        izqCam();
      else if (ByteEntrada == 107) //k
        centrarCam();
      else if (ByteEntrada == 112) //p
        paneo();
      else if (ByteEntrada == 108) //l
        derCam();
      else if (ByteEntrada == 119) //w
        adelante();
      else if (ByteEntrada == 115 ){ //s
        if (sw==0)
           atras();
        else
           parar_total();
      }
      else if (ByteEntrada == 97) //a
      {
        izq();  
        delay(200);
        parar_total();
      }
      else if (ByteEntrada == 101) //e
        parar_total();  
      else if (ByteEntrada == 100)//d
      {
        der();
        delay(200);
        parar_total();
      } 
      else if (ByteEntrada == 45) // -
        velocidad_val=(velocidad_val <= 0)?0:(velocidad_val - 5);
      else if (ByteEntrada == 43)// +
        velocidad_val=(velocidad_val >= 255)?255:(velocidad_val + 5);
      //else
        //parar_total();
     
  } 
} 
