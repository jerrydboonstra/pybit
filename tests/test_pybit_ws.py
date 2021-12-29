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
    """
    on_open: function
        Callback object which is called at opening websocket.
        on_open has one argument.
        The 1st argument is this class object.
    on_message: function
        Callback object which is called when received data.
        on_message has 2 arguments.
        The 1st argument is this class object.
        The 2nd argument is utf-8 data received from the server.
    on_error: function
        Callback object which is called when we get error.
        on_error has 2 arguments.
        The 1st argument is this class object.
        The 2nd argument is exception object.
    on_close: function
        Callback object which is called when connection is closed.
        on_close has 3 arguments.
        The 1st argument is this class object.
        The 2nd argument is close_status_code.
        The 3rd argument is close_msg.
    on_cont_message: function
        Callback object which is called when a continuation
        frame is received.
        on_cont_message has 3 arguments.
        The 1st argument is this class object.
        The 2nd argument is utf-8 string which we get from the server.
        The 3rd argument is continue flag. if 0, the data continue
        to next frame data
    on_data: function
        Callback object which is called when a message received.
        This is called before on_message or on_cont_message,
        and then on_message or on_cont_message is called.
        on_data has 4 argument.
        The 1st argument is this class object.
        The 2nd argument is utf-8 string which we get from the server.
        The 3rd argument is data type. ABNF.OPCODE_TEXT or ABNF.OPCODE_BINARY will be came.
        The 4th argument is continue flag. If 0, the data continue
    """

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
