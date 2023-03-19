FROM python:3.11.2-bullseye

RUN useradd -ms /bin/bash quizmaster
USER quizmaster
WORKDIR /home/quizmaster

COPY ./requirements.txt ./
COPY ./src ./src

RUN python3 -m pip install --upgrade pip && \
  pip install --user -r requirements.txt --no-cache-dir && \
  pip cache purge

CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0"]
