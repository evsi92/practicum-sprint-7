FROM python:3.12-slim

# Установим системные зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Рабочая директория
WORKDIR /app

# Скопируем зависимости
COPY requirements.txt .

# Установим Python-зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Скопируем исходники проекта
COPY . .

# Запуск REPL (можно заменить на API, если будет FastAPI)
CMD ["python", "src/repl.py"]