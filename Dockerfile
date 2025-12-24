FROM jrottenberg/ffmpeg:6.1-alpine

# install python + pip
RUN apk add --no-cache python3 py3-pip

WORKDIR /app

# copy app
COPY app.py .

# install server deps
RUN pip install fastapi uvicorn python-multipart

# expose render port
EXPOSE 10000

# start server
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "10000"]
