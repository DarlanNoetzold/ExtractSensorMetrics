FROM python:3.9-slim

WORKDIR /app

# Instalar cron e outras dependências
RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

# Copiar o requirements.txt e instalar dependências
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante dos arquivos para o contêiner
COPY . /app

# Adicionar o script ao cron jobs
RUN echo "0 0 * * * python /app/extract_metrics.py >> /var/log/cron.log 2>&1" >> /etc/crontab

# Start cron service
CMD cron -f
