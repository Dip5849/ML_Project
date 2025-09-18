# Base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies needed to compile packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential python3-dev libpq-dev libffi-dev libssl-dev gfortran curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy everything into the container
COPY . .

# Upgrade pip
RUN pip install --upgrade pip

# Install your local package (setup.py)
RUN pip install .

# Install any extra dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose ports
EXPOSE 8000 8501

# Start both FastAPI and Streamlit
CMD ["sh", "-c", "uvicorn api.api:app --host 0.0.0.0 --port 8000 & streamlit run app/app.py --server.port=8501 --server.address=0.0.0.0"]

