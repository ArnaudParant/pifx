FROM python:3.6

ADD requirements.txt .
RUN pip3 install -r requirements.txt && \
    rm requirements.txt

WORKDIR /

ADD src /src
ADD COMMIT_INFO .

ENV PYTHONPATH $PYTHONPATH:/src

ADD docker-entrypoint.sh /docker-entrypoint.sh

EXPOSE 9100
ENTRYPOINT ["/docker-entrypoint.sh"]