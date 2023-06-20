
##########################################
# 一般的な3レイヤーWebアプリケーションサーバー #
##########################################

# 構成
# 1. リバースプロキシー Web Server : Nginx, Let's Encrypt
# 2. App Server : Django, Gunicorn
# 3. DB : PostgreSQL

# Base Image
From arm64v8/ubuntu:20.04
# From amd64/ubuntu:20.04

# Author
Label author="inoue.shinichi.1800@gmail.com"

# User management
USER root
# RUN useradd -m \
#     -G \
#     sudo \
#     shihchi

# Reflesh host's repository and install base libraries.
RUN apt update \
    && apt -y upgrade \
    && apt install -y \
    software-properties-common \
    --no-install-recommends \ 
    locales \
    curl \
    wget \
    build-essential \
    python3.9 \
    python3.9-dev \
    && apt clearn \
    && apt autoremove \
    && rm -rf /var/lib/apt/lists/*

# Define locale
# RUN localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8

# Install Python libraries
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir --upgrade wheel \
    && pip install --no-cache-dir --upgrade setuptools \
    && pip install --no-cache-dir django==3.2.19

# USER shinichi

# # Command
# CMD ["whoami"]


