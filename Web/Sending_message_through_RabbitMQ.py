import pika, os, logging, time

# Parse CLODUAMQP_URL (fallback to localhost)
url = os.environ.get('CLOUDAMQP_URL', 'amqps://yvbeowen:VURyPmCU2CQh2LwQMq9gPlZ7eQcdq6e2@puffin.rmq2.cloudamqp.com/yvbeowen')
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params) # Connect to CloudAMQP
channel = connection.channel() # start a channel
channel.queue_declare(queue='Message_broker_testing') # Declare a queue

# send a message
channel.basic_publish(exchange='', routing_key='Message_broker_testing', body='Greetings!')
print("[x] Message sent to consumer")
connection.close()




