#!/bin/sh

if [ "$ENVIRONMENT" = "production" ]; then
    exec uvicorn storage_tracker.main:app \
        --host 0.0.0.0 \
        --port 8000 \
        --ssl-keyfile "$SSL_KEYFILE" \
        --ssl-certfile "$SSL_CERTFILE"
else
    exec uvicorn storage_tracker.main:app \
        --host 0.0.0.0 \
        --port 8000 \
        --reload
fi
