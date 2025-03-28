import pika, os, logging, time, sys
url = os.environ.get('CLOUDAMQP_URL', 'amqps://yvbeowen:VURyPmCU2CQh2LwQMq9gPlZ7eQcdq6e2@puffin.rmq2.cloudamqp.com/yvbeowen')
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel() # start a channel
channel.exchange_declare(exchange='direct_logs', exchange_type='direct') # Declare a queue

result = channel.queue_declare(queue='')
queue_name = result.method.queue

severities = sys.argv[1:]
if not severities:
    sys.stderr.write("Usage: %s [info] [warning] [error]\n" % sys.argv[0])
    sys.exit(1)

for severity in severities:
    channel.queue_bind(
        exchange='direct_logs', queue=queue_name, routing_key=severity)
print(' [*] Waiting for logs. To exit press CTRL+C')


# create a function which is called on incoming messages
def callback(ch, method, properties, body):
  print(" [x] %r:%r" % (method.routing_key, body))
  channel.basic_consume(
  queue=queue_name, on_message_callback=callback, auto_ack=True)


channel.start_consuming()
