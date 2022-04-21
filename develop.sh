#!/usr/bin/env bash

set -e

source ./.env

message() {
    echo "=> $1"
}

create-lambda-zip() {
    message "Start... Create zip lambda"
    cp lambda_function.py ./lambda-prod
    cp models.py  ./lambda-prod
    cp requirements.txt  ./lambda-prod

    cd ./lambda-prod
    USER=$(id -u)
    GRP=$(id -g)
    docker run --rm -it -u $USER:$GRP -v $(pwd):/app -w /app python:3.8 python3 -m pip install -r ./requirements.txt -t . --no-python-version-warning --disable-pip-version-check --no-input --quiet --no-cache-dir
    docker run --rm -it -v $(pwd):/app -w /app python:3.8 chown $USER:$GRP ./* -R
    find . -type f -print0 | xargs -0 chmod 644
	find . -type d -print0 | xargs -0 chmod 755
    zip -m --exclude \*.git\* -r ../lambda.zip *
    message "Created zip lambda"
}

build-python() {
    message "Rebuild python"
    docker-compose rm python
    docker-compose build python
}

bash() {
    message "Run python script"
    docker-compose run --rm python bash
}

python() {
    message "Run unittest python script"
    docker-compose run --rm python python "$@"
}

run() {
    message "Run python"
    docker-compose run --rm python python lambda_function.py
}

_help() {
    message "Usage examples: "
    IFS=$'\n'
    for f in $(declare -F); do
        ( [ "${f:9:2}" == "fx" ] || [ "${f:11:1}" == "_" ] ) && continue;
        echo "  ./develop.sh ${f:11}"
    done

    echo
}

if [ -z "$1" ]; then
    _help
    exit 1
fi

"$@"
