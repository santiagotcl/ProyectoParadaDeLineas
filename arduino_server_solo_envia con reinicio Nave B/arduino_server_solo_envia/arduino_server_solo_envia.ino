

#include <SPI.h>
#include <Ethernet.h>
#include <TimerOne.h>
#include <EEPROM.h>
#include <avr/wdt.h>

                               // Introduzca una direcciÛn MAC y la direcciÛn IP para el controlador
byte mac[] = { 
0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };
IPAddress ip(10,0,0,27);   // Esta direccion IP debe ser cambiada obligatoriamente 
                              // dependiendo de la subred de su Area Local y es la que 
                              // usara para conectarse por el Navegador.

EthernetServer server(80);    // Puerto 80 por defecto para HTTP
int contador=0;
int hora=0;
int temp=0;
int hora1=0;

int contador2=0;
int hora2=0;
int hora3=0;

String estado2;
String estado;
  
void setup() {
  wdt_disable(); // Desactivar el watchdog mientras se configura, para que no se resetee
  Ethernet.begin(mac, ip);    //inicializa la conexiÛn Ethernet y el servidor
  server.begin();
 
  pinMode(0,INPUT_PULLUP);
  pinMode(1,INPUT_PULLUP);
  pinMode(2,INPUT_PULLUP);
  pinMode(4,INPUT_PULLUP);
  pinMode(7,INPUT_PULLUP);
  pinMode(6,OUTPUT);
  digitalWrite(6,HIGH);
  Timer1.initialize(1000000);         // Dispara cada 1s
  Timer1.attachInterrupt(ISR_Blink); // Activa la interrupcion y la asocia a ISR_Blink
  temp=EEPROM.read(3);
  hora=temp;
  hora=hora*10;
  temp=EEPROM.read(2);
  hora=hora+temp;
  hora=hora*10;
  temp=EEPROM.read(1);
  hora=hora+temp;
  hora=hora*10;
  temp=EEPROM.read(0);
  hora=hora+temp;


/*EEPROM.write(0,8);
EEPROM.write(1,3);
EEPROM.write(2,7);
EEPROM.write(3,7);
EEPROM.write(4,7);
EEPROM.write(5,0);
EEPROM.write(6,8);
EEPROM.write(7,4);*/




  temp=EEPROM.read(7);
  hora2=temp;
  hora2=hora2*10;
  temp=EEPROM.read(6);
  hora2=hora2+temp;
  hora2=hora2*10;
  temp=EEPROM.read(5);
  hora2=hora2+temp;
  hora2=hora2*10;
  temp=EEPROM.read(4);
  hora2=hora2+temp;


  wdt_enable(WDTO_8S); // Configurar watchdog a cuatro segundos
                       // Puedes usar el tiempo que te convenga de la lista de arriba
  wdt_reset(); // Actualizar el watchdog para que no produzca un reinicio

 // digitalWrite(6,LOW);
  //delay(1500);
  //digitalWrite(6,HIGH);
}




void loop() {
      
     if(digitalRead(7)==0){
          digitalWrite(6,LOW);
          delay(10000);
          }
          
  wdt_reset();    
  EthernetClient cliente = server.available(); // Inicializa cliente como servidor ethernet
  wdt_reset();
  if (cliente) {
    boolean currentLineIsBlank = true;
    while (cliente.connected()) {
      if (cliente.available()) {
        char c = cliente.read();
        if (c == '\n' && currentLineIsBlank) { 
          cliente.println("HTTP/1.1 200 OK");
          cliente.println("Content-Type: text/html");   // Envia el encabezado en codigo HTML estandar
          cliente.println("Connection: close"); 
    cliente.println("Refresh: 3");  // refresca la pagina automaticamente cada 3 segundos
          cliente.println();
          cliente.println("<!DOCTYPE HTML>"); 
          cliente.println("<html>");
          cliente.println("<HEAD>");
          cliente.println("<TITLE>Ethernet Monitor</TITLE>");
          cliente.println("</HEAD>");
          cliente.println("<BODY>");
          cliente.println("<hr />");
          cliente.println("<H1>Arduino Monitor</H1>");
          cliente.println("<br />");  
          cliente.println("<H2>Monitorea horas de funcionamiento</H2>");
          cliente.println("<br />");  
          cliente.println("Lectura horometro Ethernet");  
          cliente.println("<br />");
          cliente.println("<br />");
         /* for (int puertoAnalogo = 0; puertoAnalogo < 6; puertoAnalogo++) {
            int lecturaSensor = analogRead(puertoAnalogo);   // Lee los 6 puertos analogos de A0 a A5
            cliente.print("Entrada Analoga");
            cliente.print(puertoAnalogo);
            cliente.print(" es ");
            cliente.print(lecturaSensor);
            cliente.println("<br />");       
          }
           for (int puertoDigital = 0; puertoDigital < 9; puertoDigital++) {
            int lecturaSensor = digitalRead(puertoDigital);   // Lee los puertos Digitales
            cliente.print("Entrada Digital");
            cliente.print(puertoDigital);
            cliente.print(" es ");
            cliente.print(lecturaSensor);
            cliente.println("<br />");       
          }*/

           cliente.print("<p>");
           cliente.print("Horometro de Largo B: ");
           cliente.print("</p>");
           
           cliente.print("<p>");
           cliente.print(hora);
           cliente.print("</p>");  
                   
          cliente.print("<p>");
          cliente.print(estado);
          cliente.print("</p>");
          
          cliente.print("<p>");
          cliente.println(contador);
          cliente.print("</p>");


          
           cliente.print("<p>");
           cliente.print("Horometro de Cortos C: ");
           cliente.print("</p>");
           
           cliente.print("<p>");
           cliente.print(hora2);
           cliente.print("</p>");  
                   
          cliente.print("<p>");
          cliente.print(estado2);
          cliente.print("</p>");
          
          cliente.print("<p>");
          cliente.println(contador2);
          cliente.print("</p>");












          
          cliente.println("<br />"); 
          cliente.println("Santiago Cuozzo");
          cliente.println("</html>");
          break;
        }
        if (c == '\n') {
           currentLineIsBlank = true;
        } 
        else if (c != '\r') {
           currentLineIsBlank = false;
        }

      }
    }

    
   delay(15);           // Da tiempo al Servidor para que reciba los datos 15ms
   if(digitalRead(1)==0){
   EEPROM.write(0,0);
   contador=EEPROM.read(0);
   }
   
   cliente.stop();     // cierra la conexion
  }


}









void ISR_Blink()
   { 

    wdt_reset();
    if(digitalRead(0)==0){  
    contador=contador+1;
    estado="contando";
    if(contador == 3600){
      hora=hora+1;
      hora1=hora;
      temp=hora1%10;
      EEPROM.write(0,temp);
      hora1=hora1/10;
      temp=hora1%10;
      EEPROM.write(1,temp);
      hora1=hora1/10;
      temp=hora1%10;
      EEPROM.write(2,temp);
      hora1=hora1/10;
      temp=hora1%10;
      EEPROM.write(3,temp);
      contador=0;
     // wdt_reset();
      }
    }
    else{
      estado="parado";
      wdt_reset();
      }


    if(digitalRead(2)==0){  
    contador2=contador2+1;
    estado2="contando";
    if(contador2 == 3600){
      hora2=hora2+1;
      hora3=hora2;
      temp=hora3%10;
      EEPROM.write(4,temp);
      hora3=hora3/10;
      temp=hora3%10;
      EEPROM.write(5,temp);
      hora3=hora3/10;
      temp=hora3%10;
      EEPROM.write(6,temp);
      hora3=hora3/10;
      temp=hora3%10;
      EEPROM.write(7,temp);
      contador2=0;
      //wdt_reset();
      }
    }
    else{
      estado2="parado";
      wdt_reset();
      }







      
   }
