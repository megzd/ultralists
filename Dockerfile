FROM python:3.14-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /goat-book

COPY uv.lock pyproject.toml ./
RUN uv sync --frozen --no-install-project --no-dev

ENV PATH="/goat-book/.venv/bin:$PATH"

COPY src ./src

# this tells Django to accept connections from any network interface
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8888"]

WORKDIR /goat-book/src

# required with debug turned off
RUN python manage.py collectstatic

ENV DJANGO_DEBUG_FALSE=1

CMD ["gunicorn", "--bind", ":8888", "superlists.wsgi:application"]
