from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler import events
from apscheduler.events import SchedulerEvent

from .backgraund_request import foton_request_task


def scheduler_listener(event: SchedulerEvent):
    if event.code == events.EVENT_SCHEDULER_START:
        print('start')

    if event.code == events.EVENT_SCHEDULER_SHUTDOWN:
        print('shutdown')

    if event.code == events.EVENT_SCHEDULER_PAUSED:
        print('pause')

    if event.code == events.EVENT_SCHEDULER_RESUMED:
        print('resumed')


class SchedularService:
    scheduler = AsyncIOScheduler()

    def foton_task_start(self):
        self.scheduler.add_job(foton_request_task, trigger='interval', minutes=10)
        self.scheduler.add_listener(scheduler_listener)
        self.scheduler.start()

    def foton_task_shutdown(self):
        self.scheduler.shutdown()

    def foton_task_pause(self):
        self.scheduler.pause()

    def foton_task_resume(self):
        self.scheduler.resume()

    def task_check_status(self):
        return self.scheduler.state


schedular = SchedularService()
