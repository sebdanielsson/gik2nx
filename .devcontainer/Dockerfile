FROM mcr.microsoft.com/devcontainers/python:3.12-bullseye

RUN apt update && apt upgrade -y && apt install ffmpeg libmtdev1 -y

RUN pip3 --disable-pip-version-check --no-cache-dir install --upgrade pip

COPY requirements.txt /tmp/pip-tmp/
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt && rm -rf /tmp/pip-tmp
