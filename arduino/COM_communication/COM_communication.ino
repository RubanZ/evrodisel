#include <ArduinoJson.h>


StaticJsonBuffer<200> jsonBuffer;
JsonObject& current = jsonBuffer.createObject();


String msgReq = "";

void setup() {

  Serial.begin(9600);   //setup serial
  current["flow"] = 8.2;
  current["overflow"] = 3.2;
  current["rpm"] = 500;
  current["pressure"] = 1600;
}

void loop() {
  current.printTo(Serial);
  Serial.println();

  if (Serial.available() > 0) {
    msgReq += Serial.readString ();
    if (msgReq.length()) {
      read_data(msgReq);
      msgReq = "";
    }
  }
  delay(50);
}

void read_data(String data) {
  current["rpm"] = getValue(data, ';', 0).toInt();
  current["pressure"] = getValue(data, ';', 1).toInt();
}


String getValue(String data, char separator, int index)
{
  int found = 0;
  int strIndex[] = { 0, -1 };
  int maxIndex = data.length() - 1;

  for (int i = 0; i <= maxIndex && found <= index; i++) {
    if (data.charAt(i) == separator || i == maxIndex) {
      found++;
      strIndex[0] = strIndex[1] + 1;
      strIndex[1] = (i == maxIndex) ? i + 1 : i;
    }
  }
  return found > index ? data.substring(strIndex[0], strIndex[1]) : "";
}
