#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <AsyncTCP.h>
#include <ESPAsyncWebServer.h>

AsyncWebServer server(80);


const char* ssid_access_point = "bracelet";
const char* password_access_point = "12345678";
String base_url = "http://29fa-2a00-1370-8178-99c1-adca-83b9-8382-ce38.ngrok.io";

IPAddress local_ip(192,168,1,1);
IPAddress gateway(192,168,1,1);
IPAddress subnet(255,255,255,0);


const char* PARAM_LOGIN_VK = "login_vk";
const char* PARAM_PASSWORD_VK = "password_vk";
const char* PARAM_NAME_ACCESS_POINT = "name_access_point";
const char* PARAM_PASSWORD_ACCESS_POINT = "password_access_point";

const char index_html[] PROGMEM = R"rawliteral(
<!DOCTYPE HTML><html>
<head>
    <title>ESP Input Form</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
    <body>
        <form action="/register">
            <p><b>Vk login:</b><Br>
            <input type="text" name="login_vk">
            <p><b>Vk password:</b><Br>
            <input type="text" name="password_vk">
            <p><b>ssid access point:</b><Br>
            <input type="text" name="name_access_point">
            <p><b>password access point:</b><Br>
            <input type="text" name="password_access_point">
            <p><input type="submit" value="Register">
        </form>
    </body>
</html>)rawliteral";

void notFound(AsyncWebServerRequest *request) {
    request->send(404, "text/plain", "Not found");
}

void access_point_mode(){
    WiFi.softAP(ssid_access_point, password_access_point);
    WiFi.softAPConfig(local_ip, gateway, subnet);
    IPAddress IP = WiFi.softAPIP();
    Serial.print("AP IP address: ");
    Serial.println(IP);

    server.on("/", HTTP_GET, [](AsyncWebServerRequest *request){
        request->send_P(200, "text/html", index_html);
    });

    server.on("/register", HTTP_GET, [] (AsyncWebServerRequest *request) {
        String vk_login;
        String vk_password;
        String access_point_name;
        String access_point_password;
        vk_login = request->getParam(PARAM_LOGIN_VK)->value();
        vk_password = request->getParam(PARAM_PASSWORD_VK)->value();
        access_point_name = request->getParam(PARAM_NAME_ACCESS_POINT)->value();
        access_point_password = request->getParam(PARAM_PASSWORD_ACCESS_POINT)->value();
        // Serial.println(vk_login);
        // Serial.println(vk_password);
        // Serial.println(access_point_name);
        // Serial.println(access_point_password);
        String message;
        if (vk_login == NULL || vk_password == NULL || access_point_password == NULL || password_access_point == NULL){
            Serial.println("some data is none");
            message = "please fill all fields for correct work";
        } else{
            Serial.print("all fields are fill");
            const char* ssid = access_point_name.c_str();
            const char* passphrase = access_point_password.c_str();
            WiFi.begin(ssid, passphrase);
            if (WiFi.waitForConnectResult() != WL_CONNECTED) {
                Serial.print("WiFi Failed!");
                message = "credentials for Wi-Fi are not correct please fill again"
            } else {
                Serial.print("WiFi connection success");
                HTTPClient http;
                String register_path = base_url + "/api/v1/device/register"
                http.begin(register_path.c_str());
                http.addHeader("Content-Type", "application/json");
                int httpResponseCode = http.POST("{\"vk_login\":\"" + vk_login + "\",\"vk_password\":\"" + vk_password + "\"}");
                if (httpResponseCode>0) {
                    Serial.print("HTTP Response code: ");
                    Serial.println(httpResponseCode);
                    String payload = http.getString();
                    Serial.println(payload);
                } else {
                    Serial.print("Error code: ");
                    Serial.println(httpResponseCode);
                }
            }
        }
        request->send(200, "text/html", "status of registaration: " + message +
                                        "<br><a href=\"/\">Return to Home Page and contribute data again</a>");
    });
    server.onNotFound(notFound);
    server.begin();
}

void setup() {
    Serial.begin(115200);
    access_point_mode();

}

void loop() {

}