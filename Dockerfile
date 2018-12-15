FROM python:3.6

COPY . /src
WORKDIR /src

RUN pip install -r requirements.txt
CMD python3 vkBot.py
