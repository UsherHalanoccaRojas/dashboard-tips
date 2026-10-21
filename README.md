---
title: Dashboard Propinas
emoji: 📊
colorFrom: blue
colorTo: green
sdk: static
---

# 📊 Dashboard de propinas

Dashboard interactivo construido con **Streamlit**, **Plotly** y **Seaborn**, con despliegue automático mediante **GitHub Actions** en **Hugging Face Spaces**.

🚀 **App en vivo:** [https://huggingface.co/spaces/UsherHalanoccaRojas/dashboard-tips](https://huggingface.co/spaces/UsherHalanoccaRojas/dashboard-tips)
🎥 **Video demo:** [LINK DE YOUTUBE]
📝 **Artículo en Medium:** [LINK DE MEDIUM]

## Características

- Filtros por día y sexo
- KPIs: total facturado, propina promedio y número de registros
- Gráfico interactivo (Plotly) y reporte estadístico (Seaborn)
- Pruebas automáticas con Pytest
- Despliegue continuo (CI/CD)

## Tecnologías

| Componente | Herramienta |
|---|---|
| Dashboard | Streamlit |
| Gráficos | Plotly, Seaborn, Matplotlib |
| Datos | Pandas (dataset `tips`) |
| Contenedor | Docker / Static |
| CI/CD | GitHub Actions |
| Hosting | Hugging Face Spaces |

## Ejecutar localmente

```bash
git clone https://github.com/UsherHalanoccaRojas/dashboard-tips.git
cd dashboard-tips
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Se abrirá en http://localhost:8501

## Con Docker

```bash
docker build -t dashboard-tips .
docker run -p 8501:8501 dashboard-tips
```

## Pruebas

```bash
pytest
```

## Despliegue automatizado

Cada `push` a `main` dispara el workflow `.github/workflows/deploy.yml`:

1. **test**: instala dependencias y ejecuta `pytest`.
2. **deploy**: si las pruebas pasan, publica el código en Hugging Face Spaces.

Requiere el secreto `HF_TOKEN` configurado en GitHub (Settings → Secrets and variables → Actions).

## Estructura

```
dashboard-tips/
├── app.py
├── requirements.txt
├── Dockerfile
├── README.md
├── .gitignore
├── tests/test_data.py
└── .github/workflows/deploy.yml
```

## Equipo

- Nombre 1
- Nombre 2
- Nombre 3
