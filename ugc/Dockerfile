
FROM python:3.10.4 as base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /ugc

EXPOSE 8000/tcp

RUN pip install --upgrade pip &&  \
    groupadd -r app_group &&  \
    useradd -d /app -r -g app_group app_user

COPY --chown=app_user:app_group ./requirements.txt requirements.txt
RUN pip install -r requirements.txt --no-cache-dir

COPY --chown=app_user:app_group . .

CMD ["gunicorn", "main:app", "-w", "10", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
