#!/bin/bash
# Inicia el Servidor mosquitto
if pgrep -x "mosquitto" || \
   pgrep -x "mosquitto_sub" || \
   pgrep -x "mosquitto_pub" ; then
	echo "Mosquitto activo"

else
	mosquitto -c $PREFIX/etc/mosquitto/mosquitto.conf -d
	echo "ya estaba Mosquitto activado"
fi

#mosquitto -c $PREFIX/etc/mosquitto/mosquitto.conf -d

# iniciar el archivo que captura los datos y los guarda en la base de datos
if pgrep -f "base_dato_lecturas.sh"; then
	echo "Capturador MQTT ya en Ejecución"
else
    python app.py

#	./base_dato_lecturas.sh > /dev/null 2>&1  &
	echo "Servidor MQTT Flask"
fi

#iniciar el Servidor Flask en primer plano
# Inici el servidor web Flask
