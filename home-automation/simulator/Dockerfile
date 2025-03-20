FROM python:3.10-alpine
COPY requirements.txt app/
WORKDIR /app
RUN pip install -r requirements.txt
COPY app.py .
EXPOSE 5000
ENTRYPOINT ["python3", "app.py"]