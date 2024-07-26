# setup required:
# -have iphone 15 simulator or actual iphone 15 connected
# -have idb command line interface working
# --https://github.com/facebook/idb
# --https://fbidb.io/
# --brew tap facebook/fb
# --brew install idb-companion
# --pip3 install fb-idb
# --need python3.6+ or greater. tested on python 3.10.5
# --get uuid of device from "idb list-targets"
# -ran on macbook
import os
from typing import Tuple, TextIO
import asyncio
from datetime import datetime

# ios_dut_uuid = "0DF45C42-111B-416F-9A8E-48EE2B617EED"
ios_dut_uuid = "00008101-001C302E1143001E"
folder_to_save_outputs = os.path.join(os.getcwd(), "ios_outputs")

def get_current_date_time():
    temp = datetime.now()
    return temp.strftime("%d/%m/%Y %H:%M:%S")

async def asyncio_subprocess_query(cmd: str, file: str = None) -> str:
    print(cmd)
    if not file:
        process = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT)
        output = await process.communicate()
    else:
        process = await asyncio.create_subprocess_shell(cmd, stdout=file, stderr=file)
        output = await process.communicate()
    return (output[0].decode() if output[0] else "")  + (output[1].decode() if output[1] else "")  


async def start_asyncio_subprocess(cmd: str, fh:  TextIO = None) -> asyncio.subprocess.Process:
    print(cmd)
    if not fh:
        process = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT)
        return process
    else:
        process = await asyncio.create_subprocess_shell(cmd, stdout=fh, stderr=fh)
        return process
    
async def get_screenshot_from_ios_device(ios_dut_uuid: str, path_to_save_image: str):
    cmd = f"idb screenshot {path_to_save_image} --udid {ios_dut_uuid}"
    print( await asyncio_subprocess_query(cmd) )

async def get_idb_log_process(ios_dut_uuid: str, fh_to_idb_log: str) -> asyncio.subprocess.Process:
    process = await start_asyncio_subprocess(f"idb log --udid {ios_dut_uuid}", fh_to_idb_log)
    return process

async def get_idb_log_for_duration(ios_dut_uuid: str, path_to_idb_log: str, duration: float):
    print(f"start_time: {get_current_date_time()}")
    fh_log = open(path_to_idb_log, "w+")
    log_process = await get_idb_log_process(ios_dut_uuid, fh_log)
    await asyncio.sleep(duration)
    log_process.kill()
    await log_process.wait()
    fh_log.close()
    print(f"end_time: {get_current_date_time()}")

async def test_get_idb_log_for_duration(ios_dut_uuid: str, folder_to_save_log: str, duration: float):
    path_to_idb_log = os.path.join(folder_to_save_log, "log.txt")
    if os.path.exists(path_to_idb_log):
        os.remove(path_to_idb_log)
    await get_idb_log_for_duration(ios_dut_uuid, path_to_idb_log, duration)
    assert(os.path.exists(path_to_idb_log))


async def test_get_screenshot_from_ios_device(ios_dut_uuid: str, folder_to_save_image: str):
    path_to_save_image = os.path.join(folder_to_save_image, "screenshot.png")
    if os.path.exists(path_to_save_image):
        os.remove( path_to_save_image )
    await get_screenshot_from_ios_device(ios_dut_uuid, path_to_save_image )
    assert( os.path.basename(path_to_save_image) in os.listdir(folder_to_save_image) )
        

if __name__ == "__main__":
    # asyncio.run( test_get_screenshot_from_ios_device(ios_dut_uuid, folder_to_save_outputs) )
    asyncio.run( test_get_idb_log_for_duration(ios_dut_uuid, folder_to_save_outputs, 20) )

