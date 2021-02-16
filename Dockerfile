FROM python:3.7
ADD . /app
WORKDIR /app
COPY ./config/uvicorn.py /app
RUN pip install -r config/requirements.txt
CMD ["uvicorn","app.main:app","--host", "0.0.0.0","--port","8080"]
