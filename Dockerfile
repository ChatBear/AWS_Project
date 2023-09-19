FROM python:3.11
RUN pip install poetry
WORKDIR src/

COPY src/ ./
COPY pyproject.toml ./
COPY poetry.lock ./
RUN poetry config virtualenvs.create false 
RUN poetry install 
#CMD ["uvicorn", "main:app","--reload","--port","78", "--host", "79"]


