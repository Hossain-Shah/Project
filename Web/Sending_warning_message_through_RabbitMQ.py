import pika, os, logging, time, sys

# Parse CLODUAMQP_URL (fallback to localhost)
url = os.environ.get('CLOUDAMQP_URL', 'amqps://yvbeowen:VURyPmCU2CQh2LwQMq9gPlZ7eQcdq6e2@puffin.rmq2.cloudamqp.com/yvbeowen')
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params) # Connect to CloudAMQP
channel = connection.channel() # start a channel
channel.exchange_declare(exchange='direct_logs', exchange_type='direct') # Declare a queue

# send a message
severity = sys.argv[1] if len(sys.argv) > 1 else 'alert'
message = ' '.join(sys.argv[2:]) or 'ALARM!'
channel.basic_publish(exchange='direct_logs', routing_key=severity, body=message)
print(" [x] Sent %r:%r" % (severity, message))
connection.close()





