FROM python:3.9

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir cryptography

COPY . /app

CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--reload" ]
