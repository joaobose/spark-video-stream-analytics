# Usa una imagen base de Python
FROM python:3.8-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Instala las dependencias del sistema necesarias para opencv, qt y xvfb
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libx11-6 \
    libxcb1 \
    libx11-xcb1 \
    libxcb-render0 \
    libxcb-shape0 \
    libxcb-shm0 \
    libxext6 \
    libxrender1 \
    libqt5gui5 \
    libqt5core5a \
    libqt5widgets5 \
    wget \
    xvfb

# Añadir wait-for-it script para esperar que Kafka esté listo
RUN wget https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh && \
    chmod +x wait-for-it.sh

# Copia los archivos de requisitos y los instala
COPY ../requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copia los archivos requeridos a la imagen
COPY ../src/stream_collector.py /app/
COPY ../config /app/config
COPY ../resources /app/resources

# Comando para ejecutar el script usando Xvfb
CMD ["./wait-for-it.sh", "kafka:9092", "--", "xvfb-run", "-a", "python", "stream_collector.py"]

