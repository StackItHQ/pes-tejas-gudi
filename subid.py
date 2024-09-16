from google.cloud import pubsub_v1

# Initialize client
client = pubsub_v1.SubscriberClient()

# Replace 'your-project-id' with your Google Cloud project ID
project_id = 'sheet-syncer'

# List all subscriptions
project_path = f'projects/{project_id}'
subscriptions = client.list_subscriptions(project_path)

for subscription in subscriptions:
    print(f'Subscription ID: {subscription.name.split("/")[-1]}')
