import pika
import csv
import json
import requests
import websockets
import asyncio
import environ

env = environ.Env()
environ.Env.read_env()


async def send_notification(client_id, device_id, max_hourly_consumption, total_sensor_value):
    async with websockets.connect(f'ws://127.0.0.1:8000/ws/client/{client_id}/') as websocket:
        await websocket.send(json.dumps({"notification": f"The device with ID {device_id} has consumed {total_sensor_value}kW, having exceeded its maximum hourly consumption of {max_hourly_consumption}kW!"}))
        response = await websocket.recv()
        print(response)


def create_connection():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost')
    )
    channel = connection.channel()
    return connection, channel


def prepare_channel(channel):
    channel.exchange_declare(exchange='sensors', exchange_type='fanout')

    # when we connect to Rabbit, we need an empty, freesh queue
    # creates a queue with a random name chosen by the server
    # once the consumer connection is closed, the queue is deleted, denoted by the `exclusive` flag
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange='sensors', queue=queue_name)
    return queue_name


def get_device_max_hourly_consumption(device_id):
    response = requests.get(f"http://localhost:8000/api/devices/{device_id}/")
    if response.json():
        device = response.json()
        return int(device["max_hourly_consumption"])
    return 0


msg_number = -1
prev_sensor_value = 0

def callback(ch, method, properties, body):
    global msg_number
    global prev_sensor_value

    print(json.loads(body))
    received_message = json.loads(body)
    sensor_value = received_message["measurement_value"]
    msg_number += 1

    if msg_number != 0 and msg_number % 6 == 0:
        # device_id = received_message["device_id"]
        device_id = env("DEVICE_ID")
        max_hourly_consumption = get_device_max_hourly_consumption(device_id)
        response = requests.get("http://localhost:8000/api/mappings/", params={"device": device_id})
        total_sensor_value = sensor_value - prev_sensor_value
        prev_sensor_value = sensor_value

        if response.json():
            mapping = response.json()[0]
            mapping_id = mapping["id"]
            client_id = mapping["user"]

            if total_sensor_value > max_hourly_consumption:
                # notify client through web socket
                asyncio.run(send_notification(client_id, device_id, max_hourly_consumption, total_sensor_value))
                return

            consumption_data = {
                "mapping": mapping_id,
                "consumption": total_sensor_value
            }
            print(consumption_data)

            requests.post("http://localhost:8000/api/consumptions/", consumption_data)

        sensor_value = 0


if __name__ == "__main__":
    conn = None
    channel = None
    try:
        conn, channel = create_connection()
        queue_name = prepare_channel(channel)

        channel.basic_consume(
            queue=queue_name, on_message_callback=callback, auto_ack=True)

        channel.start_consuming()
    except:
        raise
    finally:
        if conn:
            conn.close()
