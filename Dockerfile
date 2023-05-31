FROM python:3.10-alpine

RUN python -m pip install --upgrade pip

COPY pyproject.toml /app/

WORKDIR /app

RUN pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install  

COPY . /app

RUN chmod +x ./run.sh

CMD [ "./run.sh" ]


