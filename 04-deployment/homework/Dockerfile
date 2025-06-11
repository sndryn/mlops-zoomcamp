FROM agrigorev/zoomcamp-model:mlops-2024-3.10.13-slim

WORKDIR /app

COPY script.py /app

COPY Pipfile Pipfile.lock /app/

RUN pip install pipenv && pipenv install --deploy --ignore-pipfile

ENTRYPOINT ["pipenv", "run", "python", "script.py"]
