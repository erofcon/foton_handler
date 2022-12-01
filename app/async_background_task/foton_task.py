from apscheduler.schedulers.asyncio import AsyncIOScheduler
from .backgraund_request import foton_request_task

# def scheduler_listener(event: SchedulerEvent):
#     if event.code == events.EVENT_SCHEDULER_START:
#         print(f'asyncIOScheduler start {datetime.now()}')
#
#     if event.code == events.EVENT_SCHEDULER_SHUTDOWN:
#         print(f'asyncIOScheduler shutdown {datetime.now()}')
#
#     if event.code == events.EVENT_SCHEDULER_PAUSED:
#         print(f'asyncIOScheduler pause {datetime.now()}')
#
#     if event.code == events.EVENT_SCHEDULER_RESUMED:
#         print(f'asyncIOScheduler resume {datetime.now()}')


class SchedularService:
    scheduler = AsyncIOScheduler()

    def foton_task_start(self):
        self.scheduler.add_job(foton_request_task, trigger='interval', minutes=5)
        # self.scheduler.add_listener(scheduler_listener)
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
