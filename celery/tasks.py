"""Image transformation """
import io
import time
import json
from celery import Celery
from celery.utils.log import get_task_logger
from google.cloud import storage
from PIL import Image

logger = get_task_logger(__name__)

app = Celery('tasks', broker='redis://127.0.0.1:6379/0')
app.config_from_object('celeryconfig')

# testsize = 600


@app.task
def resizex(image_bucket_origin, image_bucket_path_origin, tasks):
    """This task gets a task list in json, iterates, and transform images"""
    try:
        taskstore = json.loads(tasks)
    except ValueError:
        logger.error("Invalid json")
        raise ValueError("Invalid json in task definition")
    # TODO: Verificar auth
    client = storage.Client()
    # TODO: Verificar bucket
    bucket = client.get_bucket(image_bucket_origin)
    blob = bucket.get_blob(image_bucket_path_origin)
    vfile = io.BytesIO()
    time_start = time.time()
    blob.download_to_file(vfile)
    download_time = time.time() - time_start
    logger.info("Download time: %s", download_time)
    vimage = Image.open(vfile, mode='r')
    logger.info("Format: %s", vimage.format)
    # Resize
    # TODO: write images somewhere :P
    if "resizes" in taskstore:
        logger.info("There are %d resizes:", len(taskstore["resizes"]))
        for resize in taskstore["resizes"]:
            # TODO: Hacer resize de los tamaños pequeños a partir del resize más grande
            # recuerda: lista.sort(reverse=True)
            logger.info("Resize: %s", resize["size"])
            xpercent = (resize["size"] / float(vimage.size[0]))
            ysize = int((float(vimage.size[1]) * float(xpercent)))
            time_start = time.time()
            resizeimg = vimage.resize((resize["size"], ysize), Image.ANTIALIAS)
            resize_time = time.time() - time_start
            logger.info("Resize Time: %ss", resize_time)
    else:
        logger.info("No resizes :o")
