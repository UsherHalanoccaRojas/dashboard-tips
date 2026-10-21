FROM python:3.11-slim

WORKDIR /app

# Crear usuario no root para cumplir con las reglas de seguridad de contenedores (SonarQube S6471)
RUN useradd -m -u 1000 appuser

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
