FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --upgrade pip && \
    pip install --upgrade setuptools && \
    pip install -r requirements.txt


COPY --chown=1001:1001 . /app

USER root

ENV OPEN_AI_ORG=org-xgp7cofejcakSH6WxnpULSlO
ENV OPEN_AI_KEY=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
ENV ELEVEN_LABS_API_KEY=08293822fdbfb9c0d09496c8b219337b

COPY --chown=1001:1001 ./file /app/file

USER 1001

EXPOSE 8000

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]