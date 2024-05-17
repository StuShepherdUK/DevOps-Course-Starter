FROM python:buster as base
RUN apt-get update
RUN apt-get install -y curl
ENV WEBAPP_FOLDER=/opt/todoapp
WORKDIR $WEBAPP_FOLDER
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH:"
ENV FLASK_APP=${WEBAPP_FOLDER}/todo_app/app.py
EXPOSE 5000
COPY poetry.toml .
COPY pyproject.toml .
RUN poetry install
ADD todo_app $WEBAPP_FOLDER/todo_app

FROM base as development
ENV FLASK_DEBUG=true
ENV FLASK_ENV=development
CMD [ "/root/.local/bin/poetry", "run", "flask","run","--host=0.0.0.0"]

FROM base as test
ENV FLASK_DEBUG=true
ENV FLASK_ENV=development
CMD [ "/root/.local/bin/poetry", "run", "pytest"]

FROM base as production
ENV FLASK_ENV=production
ENV FLASK_DEBUG=false
CMD [ "/root/.local/bin/poetry", "run", "flask","run","--host=0.0.0.0"]




