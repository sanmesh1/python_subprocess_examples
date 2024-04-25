import asyncio
async def main():
    cmd = "while true; do pwd; sleep 1; done"
    with open("stdout_output.txt", "w+") as fh:
        task = await asyncio.create_subprocess_shell(cmd, stdout = fh, stderr = asyncio.subprocess.STDOUT)
        await asyncio.sleep(5)
        task.kill()

asyncio.run(main())