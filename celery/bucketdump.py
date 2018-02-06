from google.cloud import storage
from tasks import resizex

bucket_test = "drinkme-test"

# TODO: Verificar auth
client = storage.Client()
# TODO: Verificar bucket
bucket = client.get_bucket(bucket_test)
iterator = bucket.list_blobs(prefix='origen/', delimiter='/')
for resource in iterator:
    resizex.delay('drinkme-test', resource.name)
