from massive import WebSocketClient
from massive.websocket.models import WebSocketMessage, Market
from typing import List

client = WebSocketClient(market=Market.Options, verbose=True)

# Options Admin / FLEX messages
client.subscribe("AD.*")  # all options exchanges
# client.subscribe("AD.302")
# client.subscribe("AD.323")


def handle_msg(msgs: List[WebSocketMessage]):
    for m in msgs:
        print(m)


client.run(handle_msg)
