from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler import events
from .backgraund_request import foton_request_task


def scheduler_listener(event: events):
    if event.code == events.EVENT_SCHEDULER_START:
        print('start')


def foton_task_start():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(foton_request_task, trigger='interval', seconds=3)
    scheduler.add_listener(scheduler_listener)
    scheduler.start()
