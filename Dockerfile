FROM python:3.8-slim

MAINTAINER SosOrg

RUN mkdir -p /usr/src/app/

COPY requirements.txt /usr/src/app/
COPY .env /usr/src/app/

RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt

WORKDIR /usr/src/app/

EXPOSE 80

CMD ["python"]
