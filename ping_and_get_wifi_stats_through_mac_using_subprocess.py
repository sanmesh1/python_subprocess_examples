import subprocess
import shlex
import asyncio

def ping_and_get_wifi_stats():
    ping_count = 5
    ping_ip = "google.com"
    ping_task = subprocess.Popen(shlex.split(f"ping -c {ping_count} {ping_ip}"), stdout=subprocess.PIPE, stderr = subprocess.STDOUT)
    
    with open("wifistats.txt", "w+") as wifi_stats_fh:
        get_wifi_stats_task = subprocess.Popen('while true; do echo "Hello"; sleep 1; done', shell = True, stdout=wifi_stats_fh, stderr = subprocess.STDOUT)
        ping_stdout, ping_stderr = ping_task.communicate()
        print(ping_stdout)
        get_wifi_stats_task.kill()
        wifi_stats_fh.seek(0)
        print(wifi_stats_fh.read())

# async def async_ping_and_get_wifi_stats():
#     ping_count = 5
#     ping_ip = "google.com"
#     ping_task = await asyncio.subprocess.create_subprocess_shell(f"ping -c {ping_count} {ping_ip}", stdout=asyncio.subprocess.PIPE, stderr = asyncio.subprocess.STDOUT)
    
#     with open("wifistats.txt", "w+") as wifi_stats_fh:
#         get_wifi_stats_task = await asyncio.subprocess.create_subprocess_shell('while true; do echo "Hello"; sleep 1; done', stdout=wifi_stats_fh, stderr = asyncio.subprocess.STDOUT)
#         ping_stdout, ping_stderr = await ping_task.communicate()
#         print(ping_stdout)
#         get_wifi_stats_task.kill()
#         wifi_stats_fh.seek(0)
#         print(wifi_stats_fh.read())

async def async_get_wifi_stats():
    stdout = ""
    try:
        while True:
            stdout += "hello\n"
            await asyncio.sleep(1)
    except asyncio.CancelledError as e:
        return stdout



async def async_ping_and_get_wifi_stats():
    ping_count = 5
    ping_ip = "google.com"
    ping_task = await asyncio.subprocess.create_subprocess_shell(f"ping -c {ping_count} {ping_ip}", stdout=asyncio.subprocess.PIPE, stderr = asyncio.subprocess.STDOUT)
    
    get_wifi_stats_task = asyncio.create_task(async_get_wifi_stats())
    ping_stdout, ping_stderr = await ping_task.communicate()
    print(ping_stdout)
    get_wifi_stats_task.cancel()
    wifistats_stdout= await get_wifi_stats_task
    print(wifistats_stdout)
    

if __name__ == "__main__":
    # ping_and_get_wifi_stats()
    asyncio.run(async_ping_and_get_wifi_stats())