#include <ESP8266WiFi.h>
#include <PubSubClient.h>

//Libreria DHT
#include <DHT11.h>

DHT11 dht11(D4);

const char *ssid = "***********";
const char *password = "***********";

// MQTT Broker settings
const char *mqtt_broker = "192.168.1.6";  
const char *mqtt_topic = "ESP8266/sensores";     

const int mqtt_port = 1883;  // MQTT port (TCP)

WiFiClient espClient;
PubSubClient mqtt_client(espClient);

String temperature;

void connectToWiFi() {
    WiFi.begin(ssid, password);
    Serial.print("Conectando al WiFi");
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("\nConectado al WiFi");
    Serial.print("IP: ");
    Serial.println(WiFi.localIP());
}

void connectToMQTTBroker() {
    while (!mqtt_client.connected()) {
        digitalWrite(D0, LOW); 
        digitalWrite(D1, HIGH);
        
        String client_id = "esp8266-client-";
        Serial.printf("Conectando a MQTT Broker %s.....\n", client_id.c_str());
        if (mqtt_client.connect(client_id.c_str())) { //, mqtt_username, NULL)) {
            Serial.println("Conectado al MQTT broker");
            mqtt_client.subscribe(mqtt_topic);
            // Publish 
            mqtt_client.publish(mqtt_topic, "Hola Jose Torres");
            digitalWrite(D0, HIGH);  
            digitalWrite(D1, LOW);

        } else {
            Serial.print("Error al conectar al Broker, rc=");
            Serial.print(mqtt_client.state());
            Serial.println(" Intentando conectar");
            delay(5000);
        }
    }
}



void setup() {
  delay(1000); 
  Serial.begin(115200);
  connectToWiFi();
  mqtt_client.setServer(mqtt_broker, mqtt_port);
  //  mqtt_client.setCallback(mqttCallback);
  connectToMQTTBroker();
  //setupOTA();

  
  pinMode(D0, OUTPUT);
  pinMode(D1, OUTPUT);

}

unsigned long actual = 0;
unsigned long anterior = 0;
//int temperatura = 0;
//int humedad = 0;

void loop() {

int temp = 0;
int hum = 0;

actual = millis();
if((actual - anterior) >= 10000){
  
  anterior = actual;
  
  float lect = dht11.readTemperatureHumidity(temp, hum);

  temperature = String(temp) + "," + String(hum);

  if (lect != DHT11::ERROR_CHECKSUM && lect != DHT11::ERROR_TIMEOUT) {

    Serial.println("Temperatura a Subir al Servidor = " + temperature);
    mqtt_client.publish(mqtt_topic, temperature.c_str());
    delay(100);  // 
    mqtt_client.loop();

    
    } else {
        // 
        Serial.println(DHT11::getErrorString(lect));
    }

    if (!mqtt_client.connected()) {
        digitalWrite(D0, LOW);  // 
        digitalWrite(D1, HIGH);

        connectToMQTTBroker();
    }
    
    //digitalWrite(D0, HIGH);  // Turn on the LED to indicate successful connection
    //temperature = String(random(0, 3000));  // Simulated temperature value
    

}
  
  
}

