# repromon

ReproNim/repromon monitoring project. The goal is to provide a core software solution to be deployed 
at Dartmouth Brain Imaging Center (DBIC) as a pilot location, to provide “online” feedback about 
ongoing data entry and acquisition (videos, MRI) as is planned to be captured and provided by the 
ReproNim projects such as ReproIn, ReproStim, ReproEvents and con/noisseur which have being developed 
separately.  

## TODO: writeup on podman/docker setup

There is a `template.env.dev` file with a configuration for a typical setup, but it has fields to fill in.
To expedite generation of the local .env.dev, you can use following command

    sed -e "s,TODO_apikey_secret,$(openssl rand -hex 32),g" \
        -e "s,TODO_apikey_salt,$RANDOM,g" \
        -e "s,TODO_token_secret_key,$(openssl rand -hex 32),g" \
        -e "s,TODO_postgres_user,repromon,g" \
        -e "s,TODO_postgres_password,pw$RANDOM$RANDOM,g" template.env.dev > .env.dev

To run the instance in a subshell (so that we do not leak those variables in the current env) use

    ( set -a &&  source ./.env.dev && podman-compose  -f docker-compose.dev.yml up -d --build  ; )

the first time to also build the image(s) and then without --build just to start

    ( set -a &&  source ./.env.dev && podman-compose  -f docker-compose.dev.yml up -d  ; )

Then you can check that all services started using  `podman ps` which should have repromon_db_1 and repromon_web_1
services.  You can see the logs using `podman logs` and the container name or id.


