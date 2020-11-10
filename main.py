import asyncio
from aioconsole import ainput

clients = []


async def timeout(command):
    time = command.split("|")[-1]
    for x in range(1,10):
        await asyncio.sleep(int(time) / 10)
        print(f"{x}0%")


class EchoServerProtocol(asyncio.Protocol):
    def __init__(self):
        super().__init__()

    def data_received(self,data):
        num = int.from_bytes(data,"little")
        if num < 10:
            print(f"{self.peername} - OP[{num}]")
        else:
            print(f"{self.peername} - SENT [{num}]")

    def connection_made(self, transport):
        self.transport = transport
        self.peername = transport.get_extra_info('peername')
        self.peername = f"{self.peername[0]}-{self.peername[1]}"
        print(f"Connection from {self.peername} [{len(clients)+1}]")
        clients.append(transport)

    def connection_lost(self,exec):
        clients.remove(self.transport)
        print(f"Closing {self.peername} [{len(clients)}]")


async def main():
    loop = asyncio.get_running_loop()
    server = await loop.create_server(EchoServerProtocol,'0.0.0.0', 9455)

    async with server:
        await server.start_serving()
        while True:
            input = await ainput("")
            if len(clients) > 0:
                print(f"Sending to {len(clients)}")
                loop.create_task(timeout(input))
                for client in clients:
                    client.write(bytes(input,encoding="utf-8"))

print("GO")
asyncio.run(main())
