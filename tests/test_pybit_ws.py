import unittest

import time
import json

from pybit import WebSocket


class WebSocketExample(WebSocket):

    def orderbook(self):
        return self.data.get('orderBook_200.100ms.BTCUSD')

    # on_message=lambda ws, msg: self._on_message(msg),
    # on_close=self._on_close(),    # on_close=lambda ws, code, msg: self._on_close(code, msg),
    # on_open=self._on_open(),      # on_open=lambda ws: self._open(),
    # on_error=lambda ws, err: self._on_error(err)

    # noinspection PyUnusedLocal
    def _on_message(self, message):
        m = json.loads(message)
        if 'topic' in m and m.get('topic') == 'orderBook_200.100ms.BTCUSD' and m.get(
                'type') == 'snapshot':
            print('Hi!')
            self.data[m.get('topic')] = m.get('data')

    # noinspection PyUnusedLocal
    def _on_error(self, error):
        print(error)

    def _on_close(self, code, msg):
        print(f"### closed {self.wsName} with status_code={code} message={msg} ###")

    def _on_open(self, ws):
        print('Submitting subscriptions...')
        ws.send(json.dumps({
            'op': 'subscribe',
            'args': ['orderBook_200.100ms.BTCUSD']
        }))


class WebSocketTest(unittest.TestCase):

    # A very simple test to ensure we're getting something from WS.
    def test_websocket_sanity(self):
        ws = WebSocket('wss://stream.bybit.com/realtime',
                       subscriptions=['instrument_info.100ms.BTCUSD'])
        self.assertNotEqual(
            ws.fetch('instrument_info.100ms.BTCUSD'),
            []
        )

    def test_websocket_success(self):
        local_ws = WebSocketExample("wss://stream.bytick.com/realtime",
                                    subscriptions=['instrument_info.100ms.BTCUSD'])
        time.sleep(5)
        # print(local_ws.orderbook())
        self.assertNotEqual(
            local_ws.orderbook(),
            []
        )
