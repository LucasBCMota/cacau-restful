#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <ArduinoJson.h>
#include <SoftwareSerial.h>

const char* ssid = "Sbornia...";
const char* password = "lauravadia";
SoftwareSerial serialMega(13, 15);

int actual_id;
bool debug = true;
void setup () {
  Serial.begin(115200);
  serialMega.begin(115200);
  WiFi.begin(ssid, password);
 
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print("Connecting..");
  }
  actual_id = -1;
}
void loop() {
  // Check WiFi Status
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    //Request to cacau-restfull actual motors state
    http.begin("192.168.0.100", 5000, "cacau/api/v1.0/state");
    int httpCode = http.GET();
    //Check the returning code
    if(httpCode > 0){
      String payload = http.getString();
      const size_t bufferSize = JSON_OBJECT_SIZE(1) + JSON_OBJECT_SIZE(2) + 2*JSON_OBJECT_SIZE(4) + JSON_OBJECT_SIZE(5) + 200;
      DynamicJsonBuffer jsonBuffer(bufferSize);
      JsonObject& root = jsonBuffer.parseObject(payload);
      JsonObject& state = root["state"];
      int id = state["id"];
      const char* title = state["title"];
      const char* description = state["description"];
      JsonObject& commands_nano1 = state["commands"]["nano1"];
      const char* commands_nano1_motor1 = commands_nano1["motor1"];
      const char* commands_nano1_motor2 = commands_nano1["motor2"];
      const char* commands_nano1_motor3 = commands_nano1["motor3"];
      const char* commands_nano1_motor4 = commands_nano1["motor4"];

      JsonObject& commands_nano2 = state["commands"]["nano2"];
      const char* commands_nano2_motor1 = commands_nano2["motor1"];
      const char* commands_nano2_motor2 = commands_nano2["motor2"];
      const char* commands_nano2_motor3 = commands_nano2["motor3"];
      const char* commands_nano2_motor4 = commands_nano2["motor4"];
      if(id != actual_id){
        actual_id = id;
        if(debug){
          Serial.print(commands_nano1_motor1);
          Serial.print(commands_nano1_motor2);
          Serial.print(commands_nano1_motor3);
          Serial.print(commands_nano1_motor4);
          Serial.print(commands_nano2_motor1);
          Serial.print(commands_nano2_motor2);
          Serial.print(commands_nano2_motor3);
          Serial.print(commands_nano2_motor4);
        }
        serialMega.print(commands_nano1_motor1);
        serialMega.print(commands_nano1_motor2);
        serialMega.print(commands_nano1_motor3);
        serialMega.print(commands_nano1_motor4);
        serialMega.print(commands_nano2_motor1);
        serialMega.print(commands_nano2_motor2);
        serialMega.print(commands_nano2_motor3);
        serialMega.print(commands_nano2_motor4);
      }
    }
    http.end();
    delay(200);
  }
  delay(1000);
}
