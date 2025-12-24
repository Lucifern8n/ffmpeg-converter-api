FROM jrottenberg/ffmpeg:6.1-alpine

RUN apk add --no-cache python3 py3-pip

WORKDIR /app
COPY app.py .

RUN pip install --break-system-packages fastapi uvicorn python-multipart

EXPOSE 10000

# 🔴 CRITICAL FIX: override ffmpeg entrypoint
ENTRYPOINT []

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "10000"]
