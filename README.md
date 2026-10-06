# Sistema de Monitoreo IoT (Android + ESP8266 + Termux + Flask)

Sistema de Internet de las Cosas (IoT) para la lectura, almacenamiento y visualización en tiempo real de datos de temperatura y humedad mediante un sensor DHT11. 

La arquitectura utiliza un microcontrolador ESP8266 que transmite las lecturas vía el protocolo MQTT a un broker local en un dispositivo Android corriendo Termux, donde un servidor web en Flask registra la información en una base de datos SQLite y la despliega en un panel interactivo.

---

## 🛠️ Arquitectura del Sistema

- **End Device / Sensor:** ESP8266 (NodeMCU/Wemos D1 Mini) + Sensor DHT11.
- **Protocolo de Comunicación:** MQTT (Broker Mosquitto).
- **Servidor Local / Gateway:** Dispositivo Android ejecutando Termux.
- **Backend:** Python (Flask + Paho-MQTT + SQLite3).
- **Frontend:** HTML5, CSS3, JavaScript (AJAX / Chart.js) embebido en plantilla Jinja2 (`templates/index.html`).

---

## 📁 Estructura del Proyecto

```text
├── .gitignore
├── README.md
├── requirements.txt
├── app.py
├── database.py
├── templates/
│   └── index.html
└── esp8266/
    └── esp8266_dht11.ino


⚙️️ Requisitos Previos
En el Dispositivo Android (Termux)

    Termux instalado y actualizado (pkg update && pkg upgrade).

    Python 3, Mosquitto y SQLite3 instalados:
    Bash

    pkg install python mosquitto sqlite -y

En el Dispositivo ESP8266

    Arduino IDE o PlatformIO.

    Librerías necesarias:

        ESP8266WiFi

        PubSubClient (para comunicación MQTT)

        DHT sensor library (Adafruit)

🚀 Instalación y Despliegue
1. Clonar el repositorio
Bash

git clone git@github.com:7luisj/Sistema-de-Monitoreo-IoT-Androit-ESP8266-Termux-Flask-.git
cd Sistema-de-Monitoreo-IoT-Androit-ESP8266-Termux-Flask-

2. Instalar dependencias de Python
Bash

pip install -r requirements.txt

3. Iniciar el Broker Mosquitto

En una sesión/pestaña de Termux:
Bash

mosquitto -c /data/data/com.termux/files/usr/etc/mosquitto/mosquitto.conf

4. Ejecutar el servidor Flask

En otra sesión/pestaña de Termux:
Bash

python app.py

Accede al dashboard web ingresando desde cualquier navegador conectado a la misma red local a:
http://<IP_DEL_CELULAR>:5000
📌 Funcionalidades

    Lectura continua y envío de datos desde el ESP8266 mediante MQTT.

    Almacenamiento persistente de datos con marca de tiempo local en SQLite.

    Panel web interactivo con actualización automática sin recargar la página (AJAX).
