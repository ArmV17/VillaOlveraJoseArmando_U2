# Imagen base
FROM python:3.11-slim

# Directorio de trabajo
WORKDIR /app

# Copiar backend
COPY backend/ ./backend
COPY frontend/ ./frontend

# Instalar dependencias
RUN pip install flask

# Exponer puerto
EXPOSE 5000

# Comando para iniciar
CMD ["python", "backend/app.py"]