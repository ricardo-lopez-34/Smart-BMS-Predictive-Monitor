#include <WiFi.h>
#include <HTTPClient.h>

String ssid = "";
String password = "";
const char* serverUrl = "http://your-dashboard-url.com/api/data";

const int voltagePin = 34;
const int tempPin = 35;

void getCredentials() {
  Serial.println("\n--- WiFi Configuration Mode ---");
  
  Serial.println("Enter SSID:");
  while (Serial.available() == 0) {}
  ssid = Serial.readStringUntil('\n');
  ssid.trim();
  Serial.println("SSID Set to: " + ssid);

  Serial.println("Enter Password:");
  while (Serial.available() == 0) {}
  password = Serial.readStringUntil('\n');
  password.trim();
  Serial.println("Password Received.");
}

void connectToWiFi() {
  if (ssid == "" || password == "") {
    getCredentials();
  }

  Serial.print("Connecting to " + ssid);
  WiFi.begin(ssid.c_str(), password.c_str());

  int retryCount = 0;
  while (WiFi.status() != WL_CONNECTED && retryCount < 20) {
    delay(500);
    Serial.print(".");
    retryCount++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\nConnected! IP: " + WiFi.localIP().toString());
  } else {
    Serial.println("\nConnection Failed. Retrying...");
    getCredentials();
  }
}

void setup() {
  Serial.begin(115200);
  delay(1000);
  connectToWiFi();
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) {
    connectToWiFi();
  }

  int rawVolt = analogRead(voltagePin);
  int rawTemp = analogRead(tempPin);

  float voltage = (rawVolt * 3.3 / 4095.0) * 2.0; 
  float temp = (rawTemp * 3.3 / 4095.0) * 100.0; 

  Serial.printf("TELEMETRY >> V: %.2fV | T: %.1fC\n", voltage, temp);

  HTTPClient http;
  http.begin(serverUrl);
  http.addHeader("Content-Type", "application/json");

  String payload = "{\"voltage\":" + String(voltage) + ",\"temp\":" + String(temp) + "}";
  int httpResponseCode = http.POST(payload);

  if (httpResponseCode > 0) {
    Serial.println("Data Synced. Code: " + String(httpResponseCode));
  } else {
    Serial.println("Sync Error: " + http.errorToString(httpResponseCode).c_str());
  }

  http.end();
  
  Serial.println("Standby for 5 seconds...");
  delay(5000);
}
