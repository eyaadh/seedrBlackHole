import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bh.helpers.cron import Cron
from bh.telegram import falcon
from pyrogram import idle


async def main():
    scheduler = AsyncIOScheduler()
    scheduler.start()
    scheduler.add_job(Cron().check_for_new_dl, 'interval', seconds=10, max_instances=10)
    await falcon.start()
    await idle()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
