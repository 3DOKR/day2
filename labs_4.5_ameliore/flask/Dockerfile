# Image "slim" (Debian) : psycopg2-binary s'y installe sans compilation, en amd64 comme en arm64
FROM python:3.12-slim
WORKDIR /code
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
EXPOSE 5000
CMD ["python", "app.py"]
