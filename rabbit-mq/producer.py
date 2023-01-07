import csv
import sys
import time
import json
import pika
import environ
import schedule
from datetime import datetime

env = environ.Env()
environ.Env.read_env()

def create_connection():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost')
    )
    channel = connection.channel()
    return connection, channel


def parse_sensor_csv(path):
    sensor_values = []
    with open(path, "r") as sensor_csv:
        csv_reader = csv.reader(sensor_csv, delimiter='\n')
        for value in csv_reader:
            sensor_values.append(value[0])
    return sensor_values


def send_messages(channel, sensor_values):
    # the rabbit-mq can send messages to an exchange
    # exchange - recevies messages from produces and pushes them to queues
    channel.exchange_declare(exchange='sensors',
                             exchange_type='fanout')
    device_id = env("DEVICE_ID")
    for value in sensor_values:
        data = {
            "device_id": int(device_id),
            "measurement_value": float(value)
        }
        print(data)
        channel.basic_publish(exchange='sensors', routing_key='', body=json.dumps(data))
        time.sleep(2)


if __name__ == "__main__":
    conn = None
    channel = None
    try:
        conn, channel = create_connection()
        sensor_values = parse_sensor_csv("rabbit-mq\sensor.csv")
        send_messages(channel, sensor_values)
    except:
        raise
    finally:
        if conn:
            conn.close()
