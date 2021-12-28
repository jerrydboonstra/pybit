import unittest
from pybit import WebSocket

ws = WebSocket('wss://stream.bybit.com/realtime',
               subscriptions=['instrument_info.100ms.BTCUSD'])


class WebSocketTest(unittest.TestCase):

    # A very simple test to ensure we're getting something from WS.
    def test_websocket(self):
        self.assertNotEqual(
            ws.fetch('instrument_info.100ms.BTCUSD'),
            []
        )
