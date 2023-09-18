# repromon 1.0

## Overview

ReproNim/repromon monitoring project. The goal is to provide a core software solution to be deployed
at Dartmouth Brain Imaging Center (DBIC) as a pilot location, to provide “online” feedback about
ongoing data entry and acquisition (videos, MRI) as is planned to be captured and provided by the
ReproNim projects such as ReproIn, ReproStim, ReproEvents and con/noisseur which have being developed
separately.

## System Setup


### Podman / Docker Environment
There is a `template.env.dev` file with a configuration for a typical setup, but it has fields to fill in.
To expedite generation of the local .env.dev, you can use following command

    sed -e "s,TODO_apikey_secret,$(openssl rand -hex 32),g" \
        -e "s,TODO_apikey_salt,$RANDOM,g" \
        -e "s,TODO_token_secret_key,$(openssl rand -hex 32),g" \
        -e "s,TODO_initial_admin_password,$(openssl rand -base64 32 | tr -d /=+ | cut -c -12),g" \
        -e "s,TODO_postgres_user,repromon,g" \
        -e "s,TODO_postgres_password,$(openssl rand -base64 32 | tr -d /=+ | cut -c -12),g" template.env.dev > .env.dev

To build and start the instance for the first time execute it in a subshell (so that we do not leak
those variables in the current env) and use:

    ( set -a &&  source ./.env.dev && podman-compose  -f docker-compose.dev.yml up -d --build  ; )

To start container instances use:

    ( set -a &&  source ./.env.dev && podman-compose  -f docker-compose.dev.yml up -d  ; )

Then you can check that all services started using:

    podman ps

which should have repromon_db_1 and repromon_web_1 services by default.

You can see the logs using these commands:

    podman logs repromon_web_1
    podman logs repromon_db_1

To open shell on web server container use:

    podman exec -it repromon_web_1 bash

To stop instances use:

    ( set -a &&  source ./.env.dev && podman-compose  -f docker-compose.dev.yml down  ; )



### Local Development Environment


## Web Application UI

### TODO: Feedback Screen UI

### TODO: Administration

### TODO: Sending Feedback Screen Message

### TODO: Testing
