#!/bin/bash

# Source the .env file if it exists
if [ -f ".env" ]; then
    source /app/.env
fi

uvicorn main:app --reload \
  --host 0.0.0.0 --port 8000 \
  --env-file .env
