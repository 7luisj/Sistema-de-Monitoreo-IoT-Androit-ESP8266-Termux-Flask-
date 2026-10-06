        

const ctx = document.getElementById('tempChart').getContext('2d');

        // Inicialización de Chart.js
        const tempChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Temperatura (°C)',
                    data: [],
                    borderColor: '#e74c3c',
                    backgroundColor: 'rgba(231, 76, 60, 0.15)',
                    fill: true,
                    tension: 0.3,
                    borderWidth: 1,
                    pointRadius: 2,
                    pointBackgroundColor: '#c0392b'
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: false,
                        title: { display: true, text: 'Temperatura (°C)' }
                    },
                    x: {
                        title: { display: true, text: 'Hora de captura' }
                    }
                }
            }
        });

// Función AJAX para actualizar los datos sin recargar la página
        async function actualizarDatos() {
            try {
                const response = await fetch('/api/datos');
                const data = await response.json();

                if (data.temperaturas.length > 0) {
                    // Actualizar el valor numérico en pantalla
                    document.getElementById('tempValue').innerText = data.temperaturas[0];
                    const ultimaFecha = data.fechas[data.fechas.length - 1];
                    document.getElementById('lastUpdated').innerText = 'Última Lectura: ' +  data.fechas[0]; //'Última lectura: ' + ul>

            document.getElementById('humedad').innerText = data.humedad[0];

                    // Actualizar datos de la gráfica
                    tempChart.data.labels = data.fechas;
                    tempChart.data.datasets[0].data = data.temperaturas;
                    tempChart.update();
                }
            } catch (error) {
                console.error('Error al obtener datos:', error);
            }
        }

// Cargar inmediatamente
        actualizarDatos();

        // Refrescar cada 60 segundos
        setInterval(actualizarDatos, 60000);
