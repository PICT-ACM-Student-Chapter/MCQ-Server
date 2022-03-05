# ---- Base python ----
FROM python:3.9-slim-bullseye AS base

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Create app directory
WORKDIR /src

# ---- Dependencies ----
FROM base AS dependencies

# Create Python virtualenv and use it
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY ./requirements.txt ./

RUN pip install -r requirements.txt --no-cache-dir


# ---- Copy Files/Build ----
FROM base

WORKDIR /src

COPY . /src

COPY --from=dependencies /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
