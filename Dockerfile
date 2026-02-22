FROM python:3.12-slim

RUN groupadd -g 1000 pygroup && useradd -u 1000 -g pygroup -s /bin/sh pyuser

WORKDIR /code

COPY requirements.txt ./

RUN pip install --no-cache-dir --upgrade -r requirements.txt

RUN mkdir -p /code/artifacts && chown pyuser:pygroup /code/artifacts

COPY --chown=pyuser:pygroup ./app ./app

ENV PYTHONPATH=/code

USER pyuser

CMD ["python", "./app/main.py"]
