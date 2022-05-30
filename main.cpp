#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <AsyncTCP.h>
#include <ESPAsyncWebServer.h>
#include <ArduinoJson.h>
#include <EEPROM.h>
// подключение необходимых библитек

AsyncWebServer server(80); // инициализрование обьекта веб сервера

const int fume_sensor_pin = 34; // пин для датчика дыма
const int mio_pin = 35; // пин для mio датчика

const char* ssid_access_point = "bracelet"; // имя WiFi сети
const char* password_access_point = "12345678"; // пароль WiFi сети
String base_url = ""; // базовый адрес api

IPAddress local_ip(192, 168, 1, 1); // настройка точки доступа
IPAddress gateway(192, 168, 1, 1);
IPAddress subnet(255, 255, 255, 0);


const char* PARAM_LOGIN_VK = "login_vk"; // переменные для входных параметров регестрации
const char* PARAM_PASSWORD_VK = "password_vk";
const char* PARAM_NAME_ACCESS_POINT = "name_access_point";
const char* PARAM_PASSWORD_ACCESS_POINT = "password_access_point";

// html для главной страницы
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

// обработчик 404 ошибки
void notFound(AsyncWebServerRequest *request) {
  request->send(404, "text/plain", "Not found");
}

// функция при работе в режиме точки доступа
void access_point_mode() {
  WiFi.softAP(ssid_access_point, password_access_point); // инициализация точки достпа и её настройка
  WiFi.softAPConfig(local_ip, gateway, subnet);
  IPAddress IP = WiFi.softAPIP();
  Serial.print("AP IP address: ");
  Serial.println(IP);

  // обработчик главной страницы
  server.on("/", HTTP_GET, [](AsyncWebServerRequest * request) {
    request->send_P(200, "text/html", index_html);
  });

  // обработчик сраницы регестрации
  server.on("/register", HTTP_GET, [] (AsyncWebServerRequest * request) {
    String vk_login;
    String vk_password;
    String access_point_name;
    String access_point_password;
    vk_login = request->getParam(PARAM_LOGIN_VK)->value(); // получение введенных данных из запроса
    vk_password = request->getParam(PARAM_PASSWORD_VK)->value();
    access_point_name = request->getParam(PARAM_NAME_ACCESS_POINT)->value();
    access_point_password = request->getParam(PARAM_PASSWORD_ACCESS_POINT)->value();
    String message;
    if (vk_login == NULL || vk_password == NULL || access_point_password == NULL || password_access_point == NULL) {
      Serial.println("some data is none"); // проверка на полноту данных
      message = "please fill all fields for correct work";
    } else {
      Serial.print("all fields are fill");
      const char* ssid = access_point_name.c_str();
      const char* passphrase = access_point_password.c_str();
      WiFi.begin(ssid, passphrase); // работа в рэжиме станции для отправки запроса на регистрацию устройства
      if (WiFi.waitForConnectResult() != WL_CONNECTED) {
        Serial.print("WiFi Failed!"); // если данные для подключения к WiFi неверны
        message = "credentials for Wi-Fi are not correct please fill again";
      } else {
        Serial.print("WiFi connection success");
        HTTPClient http; // инициализация http клиента
        Serial.print("init http client");
        String register_path = base_url + "/api/v1/device/register";
        Serial.print("begin connection");
        http.begin(register_path.c_str()); // начало соединения
        Serial.print("add headers");
        http.addHeader("Content-Type", "application/json"); // добавление необходимыхх заголовков в запрос
        int httpResponseCode = http.POST("{\"vk_login\":\"" + vk_login + "\",\"vk_password\":\"" + vk_password + "\"}"); // запрос
        delay(500);
        if (httpResponseCode > 0) {
          Serial.print("HTTP Response code: ");
          Serial.println(httpResponseCode);
          String payload = http.getString(); // получаем полезную нагрузку ввиде json ответа
          char *json = new char[payload.length() + 1];
          Serial.println(payload);
          strcpy(json, payload.c_str());
          DynamicJsonDocument doc(1024);
          deserializeJson(doc, json); // преобразуем строку с ответом в понятную для языка структуру
          String message_reasponse_registration = doc["message"];
          // обрабатываем ответ с сервера
          if (message_reasponse_registration == "wrong password for vk account") {
            message = "wrong password or login for vk account";
          } else if (message_reasponse_registration == "vk account already in use") {
            message = "wrong password or login for vk account";
          } else if (message_reasponse_registration == "user successfully create") {
            message = "you are pass registartion successfully";
            // если регестрация прошла успешно то записываем во флеш память
            // id пользователя для последующей идентификации
            // и данные для подключения к сети WiFi
            int user_id = doc["user_id"];
            EEPROM.put(0, user_id);
            EEPROM.put(1, access_point_name);
            EEPROM.put(2, access_point_password);
          }
          delete [] json;
        } else {
          Serial.print("Error code: ");
          Serial.println(httpResponseCode);
        }

      }
    }
    request->send(200, "text/html", "status of registaration: " + message +
                  "<br><a href=\"/\">Return to Home Page and contribute data again</a>"); // возврат ответа со статусом регистрации
  });
  server.onNotFound(notFound);
  server.begin(); // старт работы сервера
}

void setup() {
  Serial.begin(115200);
  int check_user_id;
  EEPROM.get(0, check_user_id); // получаем id пользователя
  // если оно равно NAN то запускаем веб сервера для прохождения регестрации
  // в ином случае пропускаем этот процесс и переходим к работе в бесконесном цикле
  if (check_user_id == NAN) {
    access_point_mode();
  } else {
    pinMode(fume_sensor_pin, INPUT);
    pinMode(mio_pin, INPUT);
  }
}

void loop() {
  int user_id;
  EEPROM.get(0, user_id);
  if (user_id != NAN) {
    int fume_value = analogRead(fume_sensor_pin); // считываем значения с датчика дыма
    if (fume_value >= 350) {
      int mio_values[15];
      for (int i = 0; i == 15; i++) { // заполняем массив данными с электромиграфического датчика
        mio_values[i] = analogRead(mio_pin);
      }
      String station_name_str;
      String station_pass_str;
      // получаем данные для подключения к сети
      EEPROM.get(1, station_name_str);
      EEPROM.get(2, station_pass_str);
      const char* ssid_station = station_name_str.c_str();
      const char* passphrase_station = station_pass_str.c_str();
      WiFi.begin(ssid_station, passphrase_station);
      if (WiFi.waitForConnectResult() != WL_CONNECTED) {
        Serial.print("WiFi Failed!");
      } else {
        Serial.print("WiFi connection success");
        HTTPClient http;
        Serial.print("init http client");
        String register_path = base_url + "/api/v1/device/analyze";
        Serial.print("begin connection");
        http.begin(register_path.c_str());
        Serial.print("add headers");
        http.addHeader("Content-Type", "application/json");
        String mio_values_arr;
        // преобразуем необходимые значения для создания json строки
        mio_values_arr += "[";
        for (int e = 0; e == 15; e++) {
          String tmp = String(mio_values[e]) +  ",";
          mio_values_arr += tmp;
        }
        mio_values_arr += "]";
        String user_id_as_str = String(user_id);
        // выполняем запрос на api для анализа и сохранения mio данных
        int httpResponseCode = http.POST("{\"user_id\":\"" + user_id_as_str + "\",\"mio_values\":\"" + mio_values_arr + "\"}");
        delay(500);
      }
    }
  }
}