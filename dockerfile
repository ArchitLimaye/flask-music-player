# Use a lightweight Python image
FROM python:3.11-slim

# ✅ Install system libraries required by OpenCV and DeepFace
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port for Render/Railway
EXPOSE 8080

# ✅ Run the app using gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:app"]
