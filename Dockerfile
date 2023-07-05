FROM python:3.10
ENV PYTHONUNBUFFERED=1

WORKDIR /code
RUN apt-get update && apt-get install -y netcat
RUN pip install pipenv

#COPY ./entrypoint.sh .
#RUN sed -i 's/\r$//g' /code/entrypoint.sh
#RUN chmod +x /code/entrypoint.sh

COPY Pipfile .
COPY Pipfile.lock .
RUN pipenv install --system --deploy

COPY . /code/