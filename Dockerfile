# Use Python 3.10 base image for ARM architecture
FROM python:3.10-slim-bullseye

# Set working directory
WORKDIR /code

# Copy requirements.txt file
COPY requirements.txt .

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libhdf5-dev \
    libatlas-base-dev \
    libopenblas-dev \
    libgl1-mesa-glx \
    liblapack-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt || \
    { echo "Failed to install dependencies"; exit 1; }

COPY . .

# CMD instruction
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
