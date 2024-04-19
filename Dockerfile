FROM python:buster
RUN apt-get update
RUN apt-get install -y curl
ENV WEBAPP_FOLDER=/opt/todoapp
RUN mkdir $WEBAPP_FOLDER
WORKDIR $WEBAPP_FOLDER
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH:"
COPY todo_app/ ./todo_app/
COPY poetry.toml .
COPY pyproject.toml .
RUN poetry install
ENV FLASK_APP=${WEBAPP_FOLDER}/todo_app/app.py
EXPOSE 5000
CMD [ "/root/.local/bin/poetry", "run", "flask","run","--host=0.0.0.0"]