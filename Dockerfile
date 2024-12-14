FROM python:3.9-slim

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar solo el archivo requirements.txt primero para aprovechar la cache de Docker
COPY requirements.txt .

# Instalar las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Ahora copiar el resto de los archivos
COPY . .

# Establecer variables de entorno para Flask
ENV FLASK_APP=app
ENV FLASK_ENV=development

# Exponer el puerto 5000 para acceder a la aplicación
EXPOSE 5000

# Comando para ejecutar la aplicación Flask
CMD ["flask", "run", "--host=0.0.0.0"]
