import asyncio
import datetime
from maintenance_container.util import loop_maintenance_task


async def block_until_done(jobs: list[asyncio.Task]):
    while True:
        if all([job.done() for job in jobs]):
            return
        try:
            await asyncio.gather(*jobs)
        except asyncio.CancelledError:
            pass


async def main():
    # Create sample scheduled jobs
    async def job():
        print('Hello, world!', flush=True)

    async def job2():
        print('Hello, world 2!', flush=True)

    async def job3():
        print('Hello, world 3!', flush=True)

    async def job4():
        await asyncio.sleep(0.7)
        print('Hello, world 4!', flush=True)

    # In practice, a job should be used to control the joblist
    async def control_job(jobs: list[asyncio.Task]):
        # Demonstrate joblist manipulation
        await asyncio.sleep(2.1)
        jobs[1].cancel()
        jobs.pop(1)
        jobs.append(loop_maintenance_task(
            datetime.timedelta(seconds=0.5, minutes=0, days=0), job3))
        await asyncio.sleep(2.1)
        jobs[0].cancel()
        await asyncio.sleep(2.1)
        for job in jobs:
            job.cancel()
        print('All jobs cancelled', flush=True)

    # Fire the jobs
    jobs = [job, job2, lambda: control_job(jobs)]
    jobs = [loop_maintenance_task(datetime.timedelta(
        seconds=1, minutes=0, days=0), job) for job in jobs]

    # Job manipulation is possible after the jobs are fired
    await asyncio.sleep(1.1)
    jobs.append(loop_maintenance_task(
        datetime.timedelta(seconds=1, minutes=0, days=0), job4))

    # Loop until all jobs done - must be the last thing to be done
    await block_until_done(jobs)


if __name__ == '__main__':
    asyncio.run(main())
