FROM python:3.11-slim

WORKDIR /app

# Crear usuario no root (SonarQube S6471)
RUN useradd -m -u 1000 appuser

# Instalar dependencias con versiones fijadas y solo binarios precompilados (SonarQube S8541, S8544)
COPY requirements.lock .
RUN pip install --no-cache-dir --only-binary :all: -r requirements.lock

# Copiar solo los archivos necesarios en lugar de COPY . . (SonarQube S6470)
COPY app.py .
COPY index.html .
COPY README.md .

RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
