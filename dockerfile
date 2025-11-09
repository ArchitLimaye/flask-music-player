# ---- Base image ----
FROM python:3.11-slim

# ---- Prevent prompts ----
ENV DEBIAN_FRONTEND=noninteractive

# ---- Set working directory ----
WORKDIR /app

# ---- Copy project files ----
COPY . /app

# ---- Install system dependencies ----
# ✅ libgl1 & libglib2.0-0 fix the OpenCV / DeepFace 'libGL.so.1' error
# ✅ ffmpeg & libsm6 handle OpenCV image I/O
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    ffmpeg \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# ---- Install Python dependencies ----
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# ---- Disable GPU/CUDA usage and suppress logs ----
ENV QT_QPA_PLATFORM=offscreen
ENV TF_CPP_MIN_LOG_LEVEL=2
ENV TF_ENABLE_ONEDNN_OPTS=0

# ---- Expose port ----
EXPOSE 8080

# ---- Run Flask app with Gunicorn ----
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:app"]
