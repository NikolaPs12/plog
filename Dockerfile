# Используем стабильный Python 3.12
FROM python:3.11.9-slim

WORKDIR /app

# Скопировать зависимости и установить их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Скопировать всё приложение
COPY . .

# Запуск через gunicorn
CMD ["gunicorn", "run:app"]
