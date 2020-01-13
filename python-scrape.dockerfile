FROM python:3.7-alpine

RUN apk update && \
    apk upgrade && \
    apk add --no-cache \
    gcc \
    libc-dev \
    libxml2-dev \
    libxslt-dev \
    bash \
    git \
    tzdata && \
    cp /usr/share/zoneinfo/Asia/Tokyo /etc/localtime && \
    apk del tzdata

RUN pip install --upgrade pip
RUN apk add ttf-freefont chromium chromium-chromedriver
RUN pip install beautifulsoup4 lxml selenium Flask