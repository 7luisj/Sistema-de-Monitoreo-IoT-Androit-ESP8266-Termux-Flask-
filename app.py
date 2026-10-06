from flask import Flask, render_template, jsonify
import sqlite3
import threading
import paho.mqtt.client as mqtt
import logging
import json

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("Servidor_ESP8266_Termux_MQTT_FLASK")


DB_NAME = "basedatos.db"
app = Flask(__name__)

#Funcion conectar a la base de datos
def conectar():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
			CREATE TABLE IF NOT EXISTS mediciones (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				fecha DATETIME DEFAULT (datetime('now', 'localtime')),
				temperatura REAL,
				humedad REAL
				)
			''')



# --- 2. LÓGICA DE CLIENTE MQTT ---
def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        log.info(f"Servidor encendio con código: {reason_code}")
        client.subscribe("ESP8266/sensores") #"ESP8266/sensores"
    else:
        print(f"Error rc={reason_code}") 

#    print("conectado")
    #client.publish("control/esp32", estado_circuito())

def on_message(client, userdata, msg):
    mensaje = msg.payload.decode('utf-8')
    if mensaje == "Hola Jose Torres":
        log.info("Datos incompletos o no numéricos: %s", mensaje)
        return
    try:
        mensaje = msg.payload.decode('utf-8')
        data = mensaje.split(",") #json.loads(mensaje)
        temp = float(data[0])
        hum = float(data[1])
        log.info("datos0 = %f", temp)
        log.info("datos1 = %f", hum)

        with sqlite3.connect(DB_NAME) as conn:
            #cursor = conn.cursor()
            conn.execute(
                "INSERT INTO mediciones (temperatura, humedad) VALUES (?, ?)",
                (temp, hum)
            )
        
        log.info("Guardado en base de Datos: %s, %s",  data[0], data[1])

    except json.JSONDecodeError as e:
        log.warning("Datos incompletos o no numéricos: %s (%s)", mensaje, e)
        return


#conexion mediante mqtt
#client = mqtt.Client()

def conectar_mqtt():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("localhost", 1883, 60)
    log.info("Esperando mensajes... Presiona Ctrl+C para salir.")
    client.loop_forever()



#Ruta a la pagina WEB principal 
@app.route('/')
def index():
#	return "<p> Hola Mundo </p>"
	return render_template('index.html')


#API: entrega los datos en JSON para graficar
@app.route('/api/datos')
def datos():

    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
# Endpoint 1: Obtener último Voltaje y Corriente
        cursor.execute('''
            SELECT fecha, temperatura, humedad
            FROM mediciones
            ORDER BY id DESC LIMIT 20
        ''')
        rows = cursor.fetchall()
    
    if rows:
        fechas = [f[0] for f in rows]
        temperaturas = [t[1] for t in rows]
        humedad =[h[2] for h in rows]
        
        ultima_temp = temperaturas[-1] if temperaturas else 0
#	print(ultima_temp)
	
    return jsonify({'fechas': fechas, 'temperaturas': temperaturas, 'ultima_temperatura': ultima_temp, 'humedad': humedad})

if __name__ == '__main__':
    mqtt_thread = threading.Thread(target=conectar_mqtt, daemon=True)
    mqtt_thread.start()
    conectar()
    app.run(host="0.0.0.0", port=5000) #, debug=False, use_reloader=False, threaded=True)
