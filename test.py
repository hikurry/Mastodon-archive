import json
from os import path
with open("outbox.json", 'r') as outbox_file:
    outbox = json.loads(outbox_file.read())
with open("actor.json", 'r') as actor_file:
    actor = json.loads(actor_file.read())

statuses = [status['object'] for status in outbox["orderedItems"]]

statuses = list(reversed(statuses))

print(statuses[0]['published'][:10])
