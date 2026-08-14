# Base Image
#FROM python:3.11-slim

# Working Directory
#WORKDIR /app

# Copy Project Files
#COPY requirements.txt .

# Install Dependencies
#RUN pip install --upgrade pip && pip install --default-timeout=1000 --no-cache-dir -r requirements.txt

# Expose FastAPI Port
#EXPOSE 7860

# Run FastAPI
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]


FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 7860

CMD ["uvicorn","main:app","--host","0.0.0.0","--port","7860"]