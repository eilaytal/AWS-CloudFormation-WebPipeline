import mysql.connector
import json
from flask import jsonify
import boto3
from botocore.exceptions import ClientError


def get_secret(secret_arn):
    """
    Retrieve secret data from AWS Secrets Manager.

    Args:
        secret_arn (str): The ARN of the secret.

    Returns:
        dict: Secret data as a dictionary.
    """
    # Extract region and secret name from ARN
    secret_name = secret_arn.split(':')[6][:-7]
    region_name = secret_arn.split(':')[3]

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        # Retrieve secret value
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # Handle exceptions
        raise e

    # Parse and return secret JSON data
    secret = get_secret_value_response['SecretString']
    return json.loads(secret)


def opendb(secret_arn):
    """
    Open a connection to MySQL database and create necessary tables.

    Args:
        secret_arn (str): The ARN of the secret containing database credentials.
    """
    # Get database info from secret
    db_info = get_secret(secret_arn)

    # MySQL connection configuration
    mysql_config = {
        'user': db_info['username'],
        'password': db_info['password'],
        'host': db_info['host']
    }

    # Connect to MySQL
    conn = mysql.connector.connect(**mysql_config)
    cursor = conn.cursor()

    # Execute queries to create database and table
    cursor.execute("CREATE DATABASE IF NOT EXISTS comm")
    cursor.execute("USE comm")
    cursor.execute("CREATE TABLE IF NOT EXISTS comm ( `idcomm` INT PRIMARY KEY AUTO_INCREMENT, value INT DEFAULT 0)")
    cursor.execute("INSERT IGNORE INTO comm (idcomm, value) VALUES (1, 0)")
    conn.commit()

    # Close cursor and connection
    cursor.close()
    conn.close()


def get_data(secret_arn):
    """
    Retrieve data from MySQL database.

    Args:
        secret_arn (str): The ARN of the secret containing database credentials.

    Returns:
        jsonify: JSON response containing the fetched data.
    """
    # Get database info from secret
    db_info = get_secret(secret_arn)

    # MySQL connection configuration
    mysql_config = {
        'user': db_info['username'],
        'password': db_info['password'],
        'host': db_info['host'],
        'database': 'comm'
    }

    try:
        # Connect to MySQL
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor()

        # Execute query to select data
        cursor.execute("SELECT value FROM comm;")
        row = cursor.fetchone()  # Fetch the value

        # Close cursor and connection
        cursor.close()
        conn.close()

        # Return fetched data as JSON response
        return jsonify({'value': row[0]})

    except Exception as e:
        # Handle exceptions
        return jsonify({'error': str(e)}), 500


def update_db(secret_arn):
    """
    Update data in MySQL database.

    Args:
        secret_arn (str): The ARN of the secret containing database credentials.
    """
    # Get database info from secret
    db_info = get_secret(secret_arn)

    # MySQL connection configuration
    mysql_config = {
        'user': db_info['username'],
        'password': db_info['password'],
        'host': db_info['host'],
        'database': 'comm'
    }

    # Connect to MySQL
    conn = mysql.connector.connect(**mysql_config)
    cursor = conn.cursor()

    # Execute query to update data
    cursor.execute("UPDATE comm SET value = value + 1 WHERE idcomm = 1")
    conn.commit()

    # Close cursor and connection
    cursor.close()
    conn.close()
