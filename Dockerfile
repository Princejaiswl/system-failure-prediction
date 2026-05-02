FROM python:3.10-slim

WORKDIR /app

# ✅ Install system dependencies first
RUN apt-get update && apt-get install -y gcc python3-dev \
    && rm -rf /var/lib/apt/lists/*

# ✅ Copy only requirements first (for caching)
COPY requirements.txt .

# ✅ Upgrade pip + install dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# ✅ Now copy project code
COPY . .

# ✅ Default command (can be overridden in docker-compose)
CMD ["python", "consumer.py"]
