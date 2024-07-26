from typing import Tuple

#subprocess imports
import subprocess
import shlex

#os.system() imports
import os

#asyncio.subprocess imports
import asyncio
import time

#asyncssh imports
import asyncssh

def run_subprocess_immediately(command: str, cwd: str = None, dont_split = False ) -> Tuple[str, str]:
    if not dont_split:    
        process = subprocess.run(shlex.split(command), text=True, capture_output=True, cwd = cwd)
    else:
        process = subprocess.run(command, text=True, capture_output=True, cwd = cwd, shell=True)
    return (process.stdout, process.stderr)

def get_subprocess(command: str, cwd: str = None, dont_split = False):
    if not dont_split:
        process = subprocess.Popen(shlex.split(command), stdout = subprocess.PIPE, stderr = subprocess.PIPE, universal_newlines=True)
    else:
        process = subprocess.Popen(command, stdout = subprocess.PIPE, stderr = subprocess.PIPE, universal_newlines=True, shell = True)
    return process

def test_subprocess_commands():

    directory_of_main = "/Users/sudhayakumar/Downloads/test"

    # cmd = "echo HelloWorld"
    # cmd = f"cd {directory_of_main}; cat ./main.py"
    cmd = f"cat ./main.py"

    # stdout, stderr = run_subprocess_immediately(cmd, dont_split = True)
    stdout, stderr = run_subprocess_immediately(cmd, cwd = directory_of_main)
    print(f"{stdout}, {stderr}")

    # process = get_subprocess(cmd, dont_split = True)
    process = get_subprocess(cmd, cwd = directory_of_main)
    stdout,stderr = process.communicate()
    print(f"{stdout}, {stderr}")

def test_os_system_commands():
    output = os.system("cd /Users/sudhayakumar/Downloads/test; cat ./main.py")
    # print(output)

async def asyncio_subprocess_func(cmd):
    process = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE) 
    return process

async def asyncio_subprocess_main_single_func():
    cmd  = "echo HelloWorld"
    process1 = await asyncio_subprocess_func(cmd)
    stdout, stderr = await process1.communicate()
    print(stdout.decode(), stderr.decode())

async def asyncio_subprocess_main_multiple_func_using_communicate():
    
    start_time = time.time()
    print(f"start_time: {start_time}")
    cmd  = "ping -c 3 google.com"
    process1 = await asyncio_subprocess_func(cmd)
    
    cmd  = "ping -c 5 google.com"
    process2 = await asyncio_subprocess_func(cmd)

    p1stdout, p1stderr = await process1.communicate()
    p2stdout, p2stderr = await process2.communicate()
    end_time = time.time()

    print(f"{p1stdout}, {p1stderr}")
    print(f"{p2stdout}, {p2stderr}")
    print(f"end_time: {end_time}")

async def ping(duration):
    process = await asyncio_subprocess_func(f"ping -c {duration} google.com")
    stdout, stderr = await process.communicate()
    print(stdout.decode(), stderr.decode())

async def asyncio_subprocess_main_multiple_func_using_gather():
    start_time = time.time()
    print(f"start_time: {start_time}")

    await asyncio.gather(*[ping(3), ping(5)])
    end_time = time.time()
    print(f"end_time: {end_time}")

async def asyncio_subprocess_kill_in_between():
    start_time = time.time()
    print(f"start_time: {start_time}")
    cmd  = "ping -c 10 google.com"
    process = await asyncio_subprocess_func(cmd)
    while time.time()-start_time< 5:
        await asyncio.sleep(0.5)
    process.kill()
    stdout, stderr = await process.communicate()
    print(stdout.decode(), stderr.decode())
    end_time = time.time()
    print(f"end_time: {end_time}")

async def asyncssh_func(cmd):
    output = (None, None)
    async with asyncssh.connect('localhost') as conn:
        result = await conn.run(cmd, check=True)
        # print(result.stdout, end='')
        output = (result.stdout, result.stderr)
    return output

async def asyncssh_example():
    start_time = time.time()
    print(f"{start_time}")
    p1 = asyncio.create_task(asyncssh_func("ping -c 10 google.com"))
    p2 = asyncio.create_task(asyncssh_func("ping -c 10 google.com"))
    out1 = await p1
    out2 = await p2
    print(f"{out1}, {out2}")
    end_time = time.time()
    print(f"{end_time}")

async def asyncio_subprocess_query(cmd):
    process = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT)
    stdout, stderr = await process.communicate()
    return stdout.decode()

async def asyncio_asyncssh_query(cmd):
    output = ""
    async with asyncssh.connect('localhost') as conn:
        result = await conn.run(cmd, check=True)
        output = result.stdout + result.stderr
    return output

async def get_list_of_times_every_1_second(duration: int):
    start_time = time.time()
    with open("list_of_times.txt", "w+") as fh:
        while (time.time()-start_time < duration):
            fh.write(f"{str(round(time.time()))}\n")
            await asyncio.sleep(1)
    

async def simultaneous_ping_and_get_time_in_real_time():
    start_time = time.time()
    print(f"start_time: {start_time}")
    task1 = asyncio.create_task(asyncio_subprocess_query("ping -c 10 google.com"))
    task2 = asyncio.create_task(asyncio_asyncssh_query("ping -c 5 google.com"))
    task3 = asyncio.create_task(get_list_of_times_every_1_second(7))
    result = await asyncio.gather(*[task1, task2, task3])
    print(result)
    end_time = time.time()
    print(f"end_time: {end_time}")

def test_asyncio_subprocess_commands():
    # asyncio.run(asyncio_subprocess_main_single_func())
    # asyncio.run(asyncio_subprocess_main_multiple_func_using_communicate())
    # asyncio.run(asyncio_subprocess_main_multiple_func_using_gather())
    # asyncio.run(asyncio_subprocess_kill_in_between())
    asyncio.run(asyncssh_example())
    # asyncio.run(simultaneous_ping_and_get_time_in_real_time())



if __name__ == "__main__":
    # test_subprocess_commands()
    # test_os_system_commands()
    test_asyncio_subprocess_commands()

