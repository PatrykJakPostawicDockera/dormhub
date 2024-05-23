import asyncio
import datetime


async def _run(interval: datetime.timedelta, job: callable):
    while True:
        await asyncio.sleep(interval.total_seconds())
        await job()


def loop_maintenance_task(interval: datetime.timedelta, job: callable) -> asyncio.Task:
    return asyncio.create_task(_run(interval, job))
