import asyncio
from aioconsole import ainput

clients = []


class EchoServerProtocol(asyncio.Protocol):
    def __init__(self):
        super().__init__()

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
                for client in clients:
                    client.write(bytes(input,encoding="utf-8"))


asyncio.run(main())
