import asyncio
import re
import pandas as pd
#clear logcat, start collecting logcat, ping google.com for 10 seconds while collecting device wlan connection status, and then kill logcat and send to file.

adb_serial = "2xxxxxxxxxx"

async def async_query(cmd, file = None):
    if not file:
        process = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT)
        output = await process.communicate()
        return output[0].decode()
    else:
        process = await asyncio.create_subprocess_shell(cmd, stdout=file, stderr=file)
        output = await process.communicate()
        return output[0].decode()        

async def clear_logcat():
    output = await async_query(f"adb -s {adb_serial} logcat -c")
    print(output)

async def start_logcat_collection(file_location):
    fh = None
    try:
        cmd = f"adb -s {adb_serial} logcat -b all"
        print(cmd)
        fh = open(file_location, "w+")
        process = await asyncio.create_subprocess_shell(cmd, stdout=fh)
        await process.communicate()
    except asyncio.CancelledError:
        process.kill()
        await asyncio.sleep(1)
    
async def start_wifi_stat_collection():
    df_dict = {"SSID": [], "freq": []}
    try:
        while True:
            output = await async_query(f"adb -s {adb_serial} shell \" iw dev wlan0 link\" " )
            output = re.findall(r"SSID: +(\w+)[\s\S]+?freq: (\d+)", output)
            for out in output:
                df_dict["SSID"].append(out[0])
                df_dict["freq"].append(out[1])
            # print(output)
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        df = pd.DataFrame(df_dict)
        df.to_csv("wifi_stats.csv")
        print("Done")

async def asyncio_main():
    await clear_logcat()
    logcat_task = asyncio.create_task(start_logcat_collection("logcat.txt"))
    wlan_task = asyncio.create_task(start_wifi_stat_collection())
    # ping_task = asyncio.create_task(start_ping())
    await asyncio.sleep(3)
    # ping_output = await ping_task
    wlan_task.cancel()
    logcat_task.cancel()

    # print(ping_output)

if __name__ == "__main__":
    asyncio.run(asyncio_main())
