FROM python:3.8.2

ADD ./docker/setupfiles/requirements.txt /
RUN pip install -r requirements.txt

ADD ./docker/setupfiles/entry_point.sh /

RUN mkdir /app

ADD ./app/ /app
CMD ["/entry_point.sh"]
