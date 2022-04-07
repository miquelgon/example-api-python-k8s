FROM python:3.8.1-slim-buster

WORKDIR /usr/src/appapi
COPY requirements.txt ./
RUN pip install --no-cache-dir --disable-pip-version-check -r requirements.txt \
  && mkdir /usr/src/appapi/conf \
  && mkdir /usr/src/appapi/log 

COPY *.py ./
CMD [ "python", "./appapi.py" ]
EXPOSE 8080