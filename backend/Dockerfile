FROM  python:3.10.5-alpine

WORKDIR /usr/src/backend

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apk update \
       && apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

RUN apk add --no-cache \
gcc \
libc-dev \
geos-dev \
&& pip install shapely

COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/backend/entrypoint.sh
RUN chmod +x /usr/src/backend/entrypoint.sh

COPY . .

EXPOSE 8000
ENTRYPOINT ["/usr/src/backend/entrypoint.sh"]


CMD python manage.py makemigrations 

