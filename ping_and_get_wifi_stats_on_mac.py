# ping for 5 seconds and get wifi ssid using "networksetup -getairportnetwork en0 " on a macbook which outputs "Current Wi-Fi Network: sample_ssid_name"
import asyncio
import re
import time
async def query(cmd):
    task = await asyncio.create_subprocess_shell(cmd, stdout = asyncio.subprocess.PIPE, stderr = asyncio.subprocess.STDOUT)
    stdout, stderr = await task.communicate()
    return stdout.decode()

async def get_ssid_every_second_task():
    # return [], []
    start_time = time.time()
    time_s = []
    ssids = []
    i = 0
    try:
        while True:
            time_s.append(time.time()-start_time)
            ssid_output = await query("networksetup -getairportnetwork en0")
            ssid = re.findall(r"Network: ([\s\S]+)", ssid_output)
            ssids.append(ssid)
            # ssid.append(i)
            # i += 1
            await asyncio.sleep(1)
    except asyncio.CancelledError as e:
        return time_s, ssids
    
def extract_rtt_from_ping_rtt(ping_string):
    # return 0
    matches = re.findall(r"stddev = ([\d.]+)\/", ping_string)
    if matches == []:
        return 0
    else:
        return matches[0]
    
async def ping_from_pc(ip, count):
    stdout = await query(f"ping -c {count} {ip}")
    ping_rtt = extract_rtt_from_ping_rtt(stdout)
    return ping_rtt

async def ping_and_get_wifi_stats():
    wifi_stats_task = asyncio.create_task(get_ssid_every_second_task() ) 
    ping_task = asyncio.create_task(ping_from_pc("google.com", 5) )
    ping_rtt = await ping_task
    wifi_stats_task.cancel()
    time, ssid = await wifi_stats_task
    print(f"time: {time}")
    print(f"ssid: {ssid}")
    print(f"ping rtt = {ping_rtt}")
    
if __name__ == "__main__":
    asyncio.run(ping_and_get_wifi_stats())