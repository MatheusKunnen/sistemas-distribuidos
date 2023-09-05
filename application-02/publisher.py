import pika
import psutil
import time
import argparse


def get_arg_parser():
    parser = argparse.ArgumentParser(prog="System stats publisher")
    parser.add_argument('--host', default='localhost', action='store', help="RabbitMQ server host.")
    parser.add_argument('--exchange', default='default_pc', action='store', help="RabbitMQ exchange name.")
    parser.add_argument('--topic', required=True, action='store', help="Topics: cpu.usage_pct cpu.load1 cpu.load5 cpu.load15 ram.usage_pct.")
    parser.add_argument('--interval', default=0.1, action='store', help="Interval between messages.")
    return parser

def get_rabbitmq_connection_channel(host, exchange):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
    
    channel = connection.channel()
    channel.exchange_declare(exchange=exchange, exchange_type='topic')
    
    return connection, channel

def get_message_data(topic):
    if topic == 'cpu.usage_pct':
        return psutil.cpu_percent()
    elif topic == 'cpu.load1':
        return psutil.getloadavg()[0]
    elif topic == 'cpu.load5':
        return psutil.getloadavg()[1]
    elif topic == 'cpu.load15':
        return psutil.getloadavg()[2]
    elif topic == 'ram.usage_pct':
        return psutil.virtual_memory().percent
    else:
        raise ValueError('Invalid topic :(')

def main(host, exchange, topic, interval):
    connection, channel = get_rabbitmq_connection_channel(host, exchange)
    try:
        while True:
            message = get_message_data(topic)
            channel.basic_publish(exchange=exchange, routing_key=topic, body=str(message))
            print(f"[INFO] Message send: {topic} {message}")
            time.sleep(interval)
    finally:
        connection.close()
    

if __name__ == '__main__':
    parser = get_arg_parser()
    args = parser.parse_args()
    main(args.host, args.exchange, args.topic, float(args.interval))