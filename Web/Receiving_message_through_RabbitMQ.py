import pika, os, logging, time
url = os.environ.get('CLOUDAMQP_URL', 'amqps://yvbeowen:VURyPmCU2CQh2LwQMq9gPlZ7eQcdq6e2@puffin.rmq2.cloudamqp.com/yvbeowen')
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel() # start a channel
channel.queue_declare(queue='Message_broker_testing') # Declare a queue


# create a function which is called on incoming messages
def callback(ch, method, properties, body):
  print(" [x] Received %r" % body)


channel.basic_consume(queue='Message_broker_testing', on_message_callback=callback, auto_ack=True)
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
