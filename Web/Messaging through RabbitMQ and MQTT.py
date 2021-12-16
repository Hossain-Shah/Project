import pika, os, logging, time
logging.basicConfig()

# Parse CLODUAMQP_URL (fallback to localhost)
url = os.environ.get('CLOUDAMQP_URL', 'amqps://yvbeowen:VURyPmCU2CQh2LwQMq9gPlZ7eQcdq6e2@puffin.rmq2.cloudamqp.com/yvbeowen')
params = pika.URLParameters(url)
params.socket_timeout = 5

connection = pika.BlockingConnection(params) # Connect to CloudAMQP
channel = connection.channel() # start a channel
channel.queue_declare(queue='pdfprocess') # Declare a queue
# send a message

channel.basic_publish(exchange='', routing_key='pdfprocess', body='User information')
print ("[x] Message sent to consumer")
connection.close()


def pdf_process_function(msg):
  print(" PDF processing")
  print(" [x] Received " + str(msg))

  time.sleep(5) # delays for 5 seconds
  print(" PDF processing finished");
  return;

# Access the CLODUAMQP_URL environment variable and parse it (fallback to localhost)
url = os.environ.get('CLOUDAMQP_URL', 'amqps://yvbeowen:VURyPmCU2CQh2LwQMq9gPlZ7eQcdq6e2@puffin.rmq2.cloudamqp.com/yvbeowen')
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel() # start a channel
channel.queue_declare(queue='pdfprocess') # Declare a queue


# create a function which is called on incoming messages
def callback(ch, method, properties, body):
  pdf_process_function(body)


# set up subscription on the queue
channel.basic_consume('pdfprocess',
  callback,
  auto_ack=True)

# start consuming (blocks)
channel.start_consuming()
connection.close()