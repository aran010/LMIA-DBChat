FROM python:3.11-slim

WORKDIR /opt/ragapp/backend

# Install necessary build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    unixodbc-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip "setuptools<70.0.0" wheel
RUN pip install --no-cache-dir --no-build-isolation cx_Oracle==8.3.0
RUN sed -i '/cx_Oracle/d' requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Run FastAPI with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
