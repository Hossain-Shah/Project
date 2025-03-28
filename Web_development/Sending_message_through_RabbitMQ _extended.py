import pika, os, logging, time

# Parse CLODUAMQP_URL (fallback to localhost)
url = os.environ.get('CLOUDAMQP_URL', 'amqps://yvbeowen:VURyPmCU2CQh2LwQMq9gPlZ7eQcdq6e2@puffin.rmq2.cloudamqp.com/yvbeowen')
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params) # Connect to CloudAMQP
channel = connection.channel() # start a channel
channel.exchange_declare(exchange='logs', exchange_type='fanout')

# send a message
channel.basic_publish(exchange='logs', routing_key='', body='Integrated feature testing')
print("[x] Message sent to consumer")
connection.close()




