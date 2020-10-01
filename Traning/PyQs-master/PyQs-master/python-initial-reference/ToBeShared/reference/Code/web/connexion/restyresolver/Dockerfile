FROM registry.opensource.zalan.do/stups/python:3.6.5-22

COPY Pipfile /
COPY Pipfile.lock /

RUN pipenv install --system --deploy --ignore-pipfile

CMD mkdir -p /api

COPY api/__init__.py /api
COPY api/app.py /api

COPY resty-api.yaml /
COPY resty.py /

WORKDIR /data
CMD /resty.py