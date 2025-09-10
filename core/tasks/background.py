from celery import shared_task
import time
@shared_task
def example_background_task(x:int,y:int)->int:
    time.sleep(1); return x+y
