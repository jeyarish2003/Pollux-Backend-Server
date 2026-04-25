FROM python:3.12-slim

WORKDIR /app

# Copy requirements first (for better caching)
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy app code
COPY ./app .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000"]