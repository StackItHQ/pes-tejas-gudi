from google.cloud import pubsub_v1

# Define your Pub/Sub subscription
project_id = "sheet-syncer"
subscription_id = "https://www.googleapis.com/robot/v1/metadata/x509/admin-account%40sheet-syncer.iam.gserviceaccount.com"

# Create a Pub/Sub subscriber client
subscriber = pubsub_v1.SubscriberClient()

# Define the subscription path
subscription_path = subscriber.subscription_path(project_id, subscription_id)

# Callback to process messages
def callback(message):
    print(f"Received message: {message.data.decode('utf-8')}")
    message.ack()  # Acknowledge that the message was processed

# Subscribe to the subscription and listen for messages
streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f"Listening for messages on {subscription_path}...\n")

# Keep the main thread alive to process messages
try:
    streaming_pull_future.result()
except KeyboardInterrupt:
    streaming_pull_future.cancel()
