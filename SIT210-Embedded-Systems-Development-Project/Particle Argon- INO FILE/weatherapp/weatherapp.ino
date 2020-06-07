// This #include statement was automatically added by the Particle IDE.
#include <MQTT.h>

int connect = D7;
int ac = D4;
int heater = D5;

// Create an MQTT client
MQTT client("test.mosquitto.org", 1883, callback);


void callback(char* topic, byte* payload, unsigned int length) 
{
    if(client.isConnected()){
        
        digitalWrite(connect, HIGH);
        delay(1000);
        digitalWrite(connect, LOW);
        
    }
    
    String msg;
    
    for(int i = 0; i < length; i++){
        (char)payload[i];
        msg += (char)payload[i];
    }
    
    String value;
    
    while(value != msg){
            
        if(msg == "ac"){
            
            digitalWrite(heater, LOW);
            delay(100);
            digitalWrite(ac, HIGH);
            delay(100);
            
        }
        else if(msg == "heat"){
            
            digitalWrite(ac, LOW);
            delay(100);
            digitalWrite(heater, HIGH);
            delay(100);
            
        }
        else if(msg=="both"){
            digitalWrite(heater, LOW);
            delay(100);
            digitalWrite(ac, LOW);
            delay(100);
        }
     
        value = msg;
        
    }
   
}    
// Setup the Photon
void setup() 
{
    // Connect to the server 
    client.connect("pd");
    client.subscribe("MyWeather/ac");
    client.subscribe("MyWeather/heater");
    client.subscribe("MyWeather/both");
    
    // Configure GPIO 0 to be an input
    pinMode(0, INPUT);
    pinMode(connect, OUTPUT);
    pinMode(ac, OUTPUT);
    pinMode(heater, OUTPUT);
}


// Main loop
void loop() 
{
    client.loop();
    
}