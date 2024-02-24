from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
import time
from typing import TypedDict
from apscheduler.jobstores.base import JobLookupError
import apscheduler

def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance


@singleton
class Scheduler:
    scheduler: AsyncIOScheduler = AsyncIOScheduler()


class TaskState(TypedDict):
    try_count: int


class Task:
    def __init__(self, name, callback):
        self.name = name
        self.is_active = False
        self.note_processed = True
        self.callback = callback
        self.state: TaskState = {'try_count': 0}

    async def process_callback(self, msg):
        self.state['try_count'] = 0
        self.is_active = True
        try:
            Scheduler().scheduler.remove_job('note')
        except JobLookupError:
            pass
        self.set_notice("interval", 2)
        await self.callback(msg)

    async def process_note(self, msg):
        await self.callback(f"{self.name} note {self.state['try_count']}")
        if not self.note_processed:
            self.state['try_count'] += 1
        if self.is_active:
            await self.callback(f"{msg} {self.state['try_count']}")
        self.note_processed = False

    async def process_note_ans(self, msg):
        if self.note_processed:
            return
        if msg != "end":
            self.set_notice("interval", int(msg))
            self.state['try_count'] += 1
        else:
            self.is_active = False
            await self.callback(f"Выполнено")
            Scheduler().scheduler.remove_job('note')
        self.note_processed = True

    def set_policy_sec(self, type_trigger, secs):
        Scheduler().scheduler.add_job(self.process_callback, type_trigger, args=["Помыть пол"], seconds=secs,
                                      id=self.name + "_interval")
        if apscheduler.schedulers.base == apscheduler.schedulers.base.STATE_STOPPED:
            Scheduler().scheduler.start()

    def set_policy_date(self, datetime):
        Scheduler().scheduler.add_job(self.process_callback, 'date',run_date=datetime, args=["Помыть пол"],
                                      id=self.name + "_date")
        if apscheduler.schedulers.base == apscheduler.schedulers.base.STATE_STOPPED:
            Scheduler().scheduler.start()

    def set_notice(self, type_trigger, secs):
        try:
            Scheduler().scheduler.remove_job('note')
        except JobLookupError:
            pass
        Scheduler().scheduler.add_job(self.process_note, type_trigger, args=["Напоминание"], seconds=secs, id='note')

    @staticmethod
    def list_of_tasks():
        return [f"{job.id}, {job.trigger}" for job in Scheduler().scheduler.get_jobs()]

# task = Task("test", print)
# task.set_policy("interval", 10)
# # task.is_active = True
# # asyncio.run(task.process_callback("Помыть пол"))
#
#
# try:
#     asyncio.get_event_loop().run_forever()
# except KeyboardInterrupt:
#     pass
# finally:
#     task.scheduler.shutdown()
