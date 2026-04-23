from websockets import serve  # type: ignore
import asyncio
import json

port = 8765
subs = set()


async def mock_server(websocket):
    await websocket.send(
        '[{"ev":"status","status":"connected","message":"Connected Successfully"}]'
    )
    async for message in websocket:
        message = json.loads(message)
        if "action" not in message:
            continue
        if message["action"] == "auth":
            await websocket.send(
                '[{"ev":"status","status":"auth_success","message":"authenticated"}]'
            )
        elif message["action"] == "subscribe":
            for p in message["params"].split(","):
                subs.add(p)
                await websocket.send(
                    json.dumps(
                        [
                            {
                                "ev": "status",
                                "status": "success",
                                "message": f"subscribed to: {p}",
                            }
                        ]
                    )
                )
                await websocket.send(
                    json.dumps(
                        [
                            {
                                "ev": "T",
                                "sym": "AAPL",
                                "i": "5096",
                                "x": 10,
                                "p": 161.87,
                                "s": 300,
                                "c": [14, 41],
                                "t": 1651684192462,
                                "q": 4009402,
                                "z": 3,
                            }
                        ]
                    )
                )
                await websocket.send(
                    json.dumps(
                        [
                            {
                                "ev": "T",
                                "sym": "AMZN",
                                "i": "72815",
                                "x": 12,
                                "p": 161.87,
                                "s": 1,
                                "c": [14, 37, 41],
                                "t": 1651684192536,
                                "q": 4009408,
                                "z": 3,
                            },
                            {
                                "ev": "T",
                                "sym": "AMZN",
                                "i": "799",
                                "x": 4,
                                "p": 161.87,
                                "s": 100,
                                "t": 1651684192717,
                                "q": 4009434,
                                "z": 3,
                            },
                        ]
                    )
                )
        elif message["action"] == "unsubscribe":
            for p in message["params"].split(","):
                subs.discard(p)
                await websocket.send(
                    json.dumps(
                        [
                            {
                                "ev": "status",
                                "status": "success",
                                "message": f"unsubscribed to: {p}",
                            }
                        ]
                    )
                )


async def run_mock_server():
    async with serve(mock_server, "localhost", port):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(run_mock_server())
