# Use a lightweight base
FROM python:3.11-slim

# Install OpenCV dependencies manually
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Expose port
EXPOSE 8080

# Run app using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:app"]
