# Use slim Python image
FROM python:3.11-slim

# --- Fix OpenCV + DeepFace missing dependencies ---
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy dependency list and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all app files
COPY . .

# Expose port
EXPOSE 8080

# Start app with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:app"]
