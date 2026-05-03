FROM python:3.14-slim

# creates /venv directory
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

RUN pip install "django==6"

COPY src /src

# cd equivalent
WORKDIR /src

# this tells Django to accept connections from any network interface
CMD ["python", "manage.py", "runserver", "0.0.0.0:8888"]
