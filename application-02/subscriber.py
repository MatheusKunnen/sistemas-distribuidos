from queue import Queue
from threading import Thread

import matplotlib.pyplot as plt
import numpy as np
import argparse
import pika

msg_q = Queue()

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

def main_thread_func ():
    print("Starting main thread...")
    x = []
    y = []
    # to run GUI event loop
    plt.ion()
    
    # here we are creating sub plots
    figure, ax = plt.subplots(figsize=(10, 8))
    line1, = ax.plot(x, y)

    plt.title("TODO: Topic", fontsize=20)
    
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    
    plt.ylim([0,100])
    plt.xlim([0,100])

    while True:
        i = msg_q.get(block=True)
        print(f"Msg: {i}")

        y.append(float(i))

        if len(y) > 100:
            y.pop(0)
        else:
            x.append(len(y))
    
        plt.ylim([0,round(max(y)*1.25) if round(max(y)*1.25) < 100 else 100])

        line1.set_xdata(np.array(x))
        line1.set_ydata(np.array(y))
        ax.clear()
        ax.fill_between(x, y)
    
        figure.canvas.draw()
    
        # This will run the GUI event
        figure.canvas.flush_events()

def callback(ch, method, properties, body):
    msg_q.put(body.decode('utf-8'))

def data_thread_func (channel):
    print("Starting data thread...")
    channel.start_consuming()

def main(host, exchange, topic, ):
    connection, channel = get_rabbitmq_connection_channel(host, exchange)
    try:
        result = channel.queue_declare('', exclusive=True)
        queue_name = result.method.queue
        channel.queue_bind(exchange=exchange, queue=queue_name, routing_key=topic)
        while True:
            channel.basic_consume(
            queue=queue_name, on_message_callback=callback, auto_ack=True)
            data_t = Thread(target=data_thread_func, args=(channel,))
            data_t.start()
            main_thread_func()
    finally:
        connection.close()


if __name__ == '__main__':
    # parser = get_arg_parser()
    # args = parser.parse_args()
    # main(args.host, args.exchange, args.topic, float(args.interval))
    main('localhost', 'default_pc', 'cpu.usage_pct')