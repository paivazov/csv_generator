FROM python:3.10

WORKDIR /app

RUN python -m venv /opt/planeks
ENV VIRTUAL_ENV /opt/planeks
ENV PATH $VIRTUAL_ENV/bin:$PATH

COPY . /app

RUN pip install -U pip setuptools wheel
RUN pip install -r requirements-dev.txt
#CMD celery -A planeks_csv_generator  worker -E --loglevel=INFO

