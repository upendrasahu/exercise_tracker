FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py
ENV FLASK_DEBUG=0

EXPOSE 5001

CMD ["python", "app.py"]