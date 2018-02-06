import json
from tasks import resizex

filename = "resize.json"
bucket_test = "drinkme-test"
# Grande
# object_test = "origen/P5070761-1.jpg"
# Mediano
object_test = "origen/IMG_9072-1.jpg"

with open(filename, 'r') as f:
    try:
        datastore = json.load(f)
    except ValueError:
        print("Invalid json")
        exit(1)

tareas = json.dumps(datastore)
resizex.delay(bucket_test, object_test, tareas)
