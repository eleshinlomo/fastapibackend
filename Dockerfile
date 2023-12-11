FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --upgrade pip && \
    pip install --upgrade setuptools && \
    pip install -r requirements.txt

ENV OPEN_AI_ORG = 'xxx'
ENV OPEN_AI_KEY = 'xxx'
ENV ELEVEN_LABS_API_KEY = 'xxx'

COPY . /app

EXPOSE 8000

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]