import psycopg2.extras
import pytz
from datetime import datetime, timedelta
import psycopg2.extras
from psycopg2 import Error
import os
from infi.clickhouse_orm import Database
import time
import boto3
from base64 import b64decode

# BASE
BATCH_SIZE = int(os.environ.get("BATCH_SIZE") or 50)
BATCH_INSERT_SIZE = int(os.environ.get("BATCH_INSERT_SIZE") or 50)

# DEV_MODE
DEBUG = os.environ.get("DEBUG") or 1

print("Debug = " + DEBUG)


# (Optional method)
def __get_decrypted_value_aws(value: str) -> str:
    # Use only for PROD mode
    # Decrypt code should run once and variables stored outside of the function
    # handler so that these are decrypted once per container
    return boto3.client('kms').decrypt(
        CiphertextBlob=b64decode(value),
        EncryptionContext={'LambdaFunctionName': os.environ['AWS_LAMBDA_FUNCTION_NAME']}
    )['Plaintext'].decode('utf-8')


# (Optional method)
def __get_storage_password(storage_name: str) -> str:
    tokens = [True, 'true', 'True', '1', 1]
    if DEBUG in tokens:
        return os.environ.get(storage_name) or 'admin'
    else:
        return __get_decrypted_value_aws(os.environ.get(storage_name))


# (Optional method)
def __get_postgres_client() -> psycopg2.connect:
    connection = psycopg2.connect(
        host=os.environ.get('POSTGRES_HOST') or 'postgres',
        dbname=os.environ.get('POSTGRES_DB') or 'test_db_dev',
        user=os.environ.get('POSTGRES_USER') or 'postgres',
        password=__get_storage_password('POSTGRES_PASSWORD'),
        port=os.environ.get('POSTGRES_PORT') or 5432
    )
    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

    return cursor


# (Optional method)
def __get_clickhouse_client() -> Database:
    clickhouse_db = Database(
        db_name=os.environ.get('CLICKHOUSE_DB') or 'clickhouse',
        db_url=os.environ.get('CLICKHOUSE_URL') or 'http://clickhouse:8123',
        username=os.environ.get('CLICKHOUSE_USERNAME') or 'test_lambda',
        password=__get_storage_password('CLICKHOUSE_PASSWORD')
    )

    return clickhouse_db


# modify this methods (Optional method)
def handle_storage():
    start_date = datetime.now(tz=pytz.timezone('Europe/Kiev')).replace(hour=0, minute=0, second=0,
                                                                       microsecond=0) + timedelta(days=-20000)
    end_date = datetime.now(tz=pytz.timezone('Europe/Kiev')).replace(hour=0, minute=0, second=0,
                                                                     microsecond=0) + timedelta(days=-1)

    print('start_date - {0}'.format(start_date))
    print('end_date - {0}'.format(end_date))
    try:
        pg = __get_postgres_client()
        ch = __get_clickhouse_client()

        offset = 0
        limit = BATCH_SIZE
        while True:

            sql = "SELECT t.id AS id, t.name AS name, t.created_on AS created_on FROM " \
                  "test AS ur WHERE t.created_on >= %s AND t.created_on < %s " \
                  "ORDER BY t.created_on OFFSET %s LIMIT %s "

            pg.execute(sql, (start_date, end_date, offset, limit))
            pg_result: list = pg.fetchall()
            
            print("PG Results: %s" % len(pg_result))

            for item in pg_result:
                id = item['id']
                name = item['name']
                created_on = item['created_on']

                # TODO move data from POSTGRES to CLICKHOUSE

            offset = offset + BATCH_SIZE


        pg.close()
    except (Exception, Error) as error:
        print("Errors", error)


# Required main method for running lambda in AWS
def lambda_handler(event=None, context=None):
    """
    Main asw lambda_handler
    """
    handle_storage()


if __name__ == '__main__':
    """
    Write test path
    """
    start = time.time()
    lambda_handler()
    print('Time work... - ', time.time() - start, 'seconds.')
