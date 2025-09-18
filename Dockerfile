# Base image
FROM python:3.10-slim

# Install Nginx
RUN apt-get update && apt-get install -y nginx && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

# Copy dependencies and install
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY fastapi ./fastapi
COPY streamlit ./streamlit
COPY nginx.conf /etc/nginx/nginx.conf

# Expose port 80
EXPOSE 80

# Start FastAPI, Streamlit, and Nginx
CMD ["sh", "-c", "uvicorn fastapi.main:app --host 0.0.0.0 --port 8000 & streamlit run streamlit/streamlit_app.py --server.port 8501 --server.address 0.0.0.0 --server.headless true & nginx -g 'daemon off;'"]
