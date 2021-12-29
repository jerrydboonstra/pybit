import unittest
import websocket

try:
    import thread
except ImportError:
    import _thread as thread
import time
import json
import ssl
import threading

from pybit import WebSocket

ws = WebSocket('wss://stream.bybit.com/realtime', subscriptions=['instrument_info.100ms.BTCUSD'])


class WebSocketExample:
    def __init__(self):
        self.data = {}

        websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp(
            "wss://stream.bytick.com/realtime",
            on_open=self._on_open,
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close,
        )
        # Setup the thread running WebSocketApp.
        self.wst = threading.Thread(target=lambda: self.ws.run_forever(
            sslopt={"cert_reqs": ssl.CERT_NONE},
        ))

        # Configure as daemon; start.
        self.wst.daemon = True
        self.wst.start()

    def orderbook(self):
        return self.data.get('orderBook_200.100ms.BTCUSD')

    # on_message=lambda ws, msg: self._on_message(msg),
    # on_close=self._on_close(),    # on_close=lambda ws, code, msg: self._on_close(code, msg),
    # on_open=self._on_open(),      # on_open=lambda ws: self._open(),
    # on_error=lambda ws, err: self._on_error(err)

    # noinspection PyUnusedLocal
    def _on_message(self, our_ws, message):
        m = json.loads(message)
        if 'topic' in m and m.get('topic') == 'orderBook_200.100ms.BTCUSD' and m.get(
                'type') == 'snapshot':
            print('Hi!')
            self.data[m.get('topic')] = m.get('data')

    # noinspection PyUnusedLocal
    def _on_error(self, our_ws, error):
        print(error)

    def _on_close(self, our_ws, close_status_code, close_message):
        print(
            f"### closed {our_ws} with status_code={close_status_code} message={close_message} ###")

    def _on_open(self, our_ws):
        print('Submitting subscriptions...')
        our_ws.send(json.dumps({
            'op': 'subscribe',
            'args': ['orderBook_200.100ms.BTCUSD']
        }))


class WebSocketTest(unittest.TestCase):

    # A very simple test to ensure we're getting something from WS.
    def test_websocket_sanity(self):
        self.assertNotEqual(
            ws.fetch('instrument_info.100ms.BTCUSD'),
            []
        )

    def test_websocket_success(self):
        local_ws = WebSocketExample()
        time.sleep(5)
        # print(local_ws.orderbook())
        self.assertNotEqual(
            local_ws.orderbook(),
            []
        )
