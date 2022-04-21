## AWS-lambda-function template ##

### What is this repository for? ###

* Running python lambda function in AWS, transfer data from POSTGRES to CLICKHOUSE, you can schedule the launch of the script to transfer the data


### Repository structure ###

* `lambda_function.py` - main file (don't rename filename and function name lambda_handler with signature)
* `./docker` - test storage (clickhouse, postgres) with init script
* `./lambda-prod` - folder for creating zip archive (PROD)
* `.env` - for testing environment (docker)
* `develop` - helper bash script
* `docker-compose.yaml` - for testing environment (docker)
* `Dockerfile` - for testing environment (docker)
* `models.py` - models file

### Create zip archive ###

```
bash develop.sh create-lambda-zip
```

### Postgres ###
You can initialize any sql scripts before starting docker container
```
./docker/postgres/init.sql
```

### Clickhouse ###
You can initialize any sql scripts before starting docker container
```
./docker/clickhouse/init.sql
```

### Build (start) applications with docker ###
```
docker-compose up -d
```

### If you need to run python script with docker ###

```
bash develop.sh python
```
or
```
docker-compose run --rm python
```

### Bash ###
```
bash develop.sh bash
```