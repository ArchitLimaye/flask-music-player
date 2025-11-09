# Use a lightweight Python base image
FROM python:3.11-slim

# Install OS-level dependencies required for OpenCV (libGL, libglib)
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy dependency file first
COPY requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy all your app files
COPY . .

# Set environment variables for safety
ENV QT_QPA_PLATFORM=offscreen
ENV TF_CPP_MIN_LOG_LEVEL=2
ENV TF_ENABLE_ONEDNN_OPTS=0

# Expose the port Railway uses
EXPOSE 8080

# Run Flask via Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:app"]
