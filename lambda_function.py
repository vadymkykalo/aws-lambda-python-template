import psycopg2.extras
import psycopg2.extras
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


# Required main method for running lambda in AWS
def lambda_handler(event=None, context=None):
    """
    Main asw lambda_handler
    """
    # TODO move data from POSTGRES to CLICKHOUSE
    # try:
    #     pg = __get_postgres_client()
    #     ch = __get_clickhouse_client()
    #
    #
    #     pg.close()
    # except (Exception, Error) as error:
    #     print("Errors", error)
    pass


if __name__ == '__main__':
    """
    Write test path
    """
    start = time.time()
    lambda_handler()
    print('Time work... - ', time.time() - start, 'seconds.')
