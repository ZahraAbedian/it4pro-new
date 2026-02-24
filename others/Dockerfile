FROM python:3.8

RUN apt-get update
RUN apt-get upgrade -y
RUN pip install Django
RUN pip install matplotlib
RUN pip install pillow
WORKDIR /app
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
