import asyncio
import websockets


class WebSocket:

    @staticmethod
    async def __send_message(server: str, message: str):
        async with websockets.connect(server) as websocket:
            await websocket.send(message)
            response = await websocket.recv()
            return response
    
    @staticmethod
    def send_message(server: str, message: str):
        res = asyncio.run(WebSocket.__send_message(server, message))
        return res

