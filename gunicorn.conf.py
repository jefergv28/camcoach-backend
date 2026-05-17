import multiprocessing
import os

# Puerto que nos asignará Render automáticamente
port = os.getenv("PORT", "8000")
bind = f"0.0.0.0:{port}"

# Número de workers recomendado: (2 * CPUs) + 1
workers = (multiprocessing.cpu_count() * 2) + 1
worker_class = "uvicorn.workers.UvicornWorker"

# Logs de producción
loglevel = "info"
accesslog = "-"
errorlog = "-"