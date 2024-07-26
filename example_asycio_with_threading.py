
# Online Python - IDE, Editor, Compiler, Interpreter
from threading import Thread
import asyncio
import time
import logging
FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)
logger = logging.getLogger()
# logger.addHandler(logging.StreamHandler())
async def get_device_mcs_every_x_seconds_and_y_duration(interval_s = 2, duration_s=7):
    start_time = time.time()
    while time.time()-start_time < duration_s:
        logger.info(f"mcs = 11, getting every {interval_s} seconds, for duration {duration_s}")
        await asyncio.sleep(interval_s)
        
async def get_iperf_throughput_every_x_seconds_and_y_duration(interval_s = 3, duration_s=7):
    start_time = time.time()
    while time.time()-start_time < duration_s:
        logger.info(f"iperf_throughput = 200, getting every {interval_s} seconds, for duration {duration_s}")
        await asyncio.sleep(interval_s)

def unlock_phone_regularly(interval_s = 1, duration_s=7):
    start_time = time.time()
    while time.time()-start_time < duration_s:
        logger.info(f"unlock phone screen, getting every {interval_s} seconds, for duration {duration_s}")
        time.sleep(interval_s)

async def async_main():
    t = Thread(target=unlock_phone_regularly, args=[3,7])
    t.start()
    task1_h = asyncio.create_task(get_device_mcs_every_x_seconds_and_y_duration())
    task2_h = asyncio.create_task(get_iperf_throughput_every_x_seconds_and_y_duration())
    result = await asyncio.gather(*[task1_h, task2_h])
    t.join()
asyncio.run(async_main())