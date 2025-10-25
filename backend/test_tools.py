import asyncio
from Jarvis_file_opner import Play_file

async def test():
    print(await Play_file("t_1_a.pdf"))

asyncio.run(test())
