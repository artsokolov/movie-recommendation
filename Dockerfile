FROM python:3.10-slim

WORKDIR /app

RUN pip install --upgrade pip

COPY pyproject.toml ./
RUN pip install .

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"] 