FROM python:3.10

RUN python -m venv /opt/planeks
ENV VIRTUAL_ENV /opt/planeks
ENV PATH $VIRTUAL_ENV/bin:$PATH
RUN pip install -U pip setuptools wheel

WORKDIR /app
