FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --upgrade pip && \
    pip install --upgrade setuptools && \
    pip install -r requirements.txt


USER root

COPY  . /app


COPY --chown=1001:1001 myFile.wav /app/myFile.wav

COPY --chown=1001:1001 stored_data.json /app/stored_data.json

ARG OPEN_AI_ORG='org-xgp7cofejcakSH6WxnpULSlO'
ARG OPEN_AI_KEY='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'
ARG ELEVEN_LABS_API_KEY='08293822fdbfb9c0d09496c8b219337b'

ENV OPEN_AI_ORG=$OPEN_AI_ORG
ENV OPEN_AI_KEY=$OPEN_AI_KEY
ENV ELEVEN_LABS_API_KEY=$ELEVEN_LABS_API_KEY


USER 1001

EXPOSE 8000

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]