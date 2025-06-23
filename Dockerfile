# Dockerfile

# Gunakan base image Python
FROM python:3.9-slim

# Set direktori kerja di dalam container
WORKDIR /app

# Salin file requirements.txt terlebih dahulu untuk caching layer
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Salin semua file dari direktori lokal ke direktori kerja di container
COPY . .

# Perintah untuk menjalankan aplikasi saat container dimulai
# --host=0.0.0.0 membuat server bisa diakses dari luar container
CMD ["flask", "run", "--host=0.0.0.0"]