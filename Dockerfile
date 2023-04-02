FROM python:3.11.2-alpine@sha256:d811538656b665bba649b3ac2c3fc8a5187e24cd510a34d7e905d7ec4534fb89


RUN apk update && \
  apk add postgresql-dev gcc musl-dev && \
  addgroup -S quizgroup && \
  adduser -S -h /home/quizmaster quizmaster -G quizgroup

USER quizmaster
WORKDIR /home/quizmaster

COPY ./requirements.txt ./
COPY ./src ./src

RUN python3 -m pip install --upgrade pip && \
  pip install --user -r requirements.txt --no-cache-dir && \
  pip cache purge

CMD [ "python3", "-m", "gunicorn", "--access-logfile=-", "--workers=2", "--threads=3",  "--worker-class=gthread", "--bind=0.0.0.0:8000", "src.app:app" ]
