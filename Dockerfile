#
# Docker file for the container of the web, worker, scheduler, and monitor services
#

FROM docker.io/debian:12
WORKDIR /app

# Install dependencies
# TODO: Consider removing the eatmydata dependency. It may not be needed.
RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends eatmydata && \
    DEBIAN_FRONTEND=noninteractive eatmydata apt-get install -y --no-install-recommends gnupg locales && \
    echo "en_US.UTF-8 UTF-8" >>/etc/locale.gen && locale-gen && \
    DEBIAN_FRONTEND=noninteractive eatmydata apt-get install -y --no-install-recommends \
      build-essential \
      libpq-dev \
      python3-dev \
      python3-pip \
      python3.11-venv \
      && \
    DEBIAN_FRONTEND=noninteractive apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

## Set user info for git (needed for datalad operations)
#RUN git config --system user.name "repromon" && \
#    git config --system user.email "repromon@example.com"
#
# RUN ["pip3", "install", "--no-cache-dir", "-U","pip", "setuptools", "poetry"]

# Some files are ignored via .dockerignore
COPY . .

RUN python3 -m venv venv && \
   venv/bin/pip install poetry && \
   venv/bin/poetry config virtualenvs.create false && \
   venv/bin/poetry config virtualenvs.in-project true && \
   venv/bin/poetry env use `which python3` && \
   venv/bin/poetry install && \
   venv/bin/poetry build

# poetry run srv
