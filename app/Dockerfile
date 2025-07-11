FROM python:3.12-slim

EXPOSE 5001
WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x docker/entrypoint.sh

ENTRYPOINT ["/bin/bash", "docker/entrypoint.sh"]