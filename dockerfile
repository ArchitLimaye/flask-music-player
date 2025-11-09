# ---- Base image ----
FROM python:3.11-slim

# ---- Prevent interactive prompts ----
ENV DEBIAN_FRONTEND=noninteractive

# ---- Working directory ----
WORKDIR /app

# ---- Copy project ----
COPY . /app

# ---- Install dependencies for OpenCV / DeepFace ----
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    ffmpeg \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# ---- Python dependencies ----
RUN pip install --no-cache-dir -r requirements.txt

# ---- Environment variables to stop TensorFlow / Qt GUI issues ----
ENV QT_QPA_PLATFORM=offscreen
ENV TF_CPP_MIN_LOG_LEVEL=2
ENV TF_ENABLE_ONEDNN_OPTS=0

# ---- Expose port ----
EXPOSE 8080

# ---- Run Flask app with Gunicorn ----
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:app"]
