FROM python:3.11-slim

# Install system dependencies and httpx binary
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl unzip ca-certificates && \
    curl -sSfL https://github.com/projectdiscovery/httpx/releases/download/v1.6.9/httpx_1.6.9_linux_amd64.zip -o /tmp/httpx.zip && \
    unzip /tmp/httpx.zip -d /usr/local/bin && \
    chmod +x /usr/local/bin/httpx && \
    rm -rf /var/lib/apt/lists/* /tmp/httpx.zip

WORKDIR /app

# Install python deps first for caching
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

ENV HOST=0.0.0.0
ENV PORT=8000
EXPOSE 8000

CMD ["python", "server.py"]
