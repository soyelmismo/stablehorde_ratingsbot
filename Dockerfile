FROM python:3-alpine

# Por alguna razón, si se elimina PYTHONUNBUFFERED, no se imprimen algunos mensajes de error o información relevante...
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
WORKDIR /

COPY ratings/ /ratings
COPY requirements.txt /requirements.txt
# Instalar dependencias
RUN apk update && \
    apk add --no-cache --virtual .build-deps \
        py3-pip && \
    pip3 install --no-cache-dir -r requirements.txt && \
    apk del .build-deps && \
    rm -rf /var/cache/apk/*

CMD ["python", "-m", "ratings"]
