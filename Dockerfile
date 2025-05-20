FROM python:3.11-slim as builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /app /app

EXPOSE 5000

CMD ["newrelic-admin", "run-program", "python", "src/main.py"]

#CMD ["newrelic-admin", "run-program", "python", "main.py" "tp_devops.py"]
