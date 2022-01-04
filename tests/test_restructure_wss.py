import os
from time import sleep
import logging
import unittest

from pybit import usdt_perpetual, inverse_perpetual

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger('test')

API_KEY = os.environ.get('BYBIT_API_KEY', '')
API_SECRET = os.environ.get('BYBIT_API_SECRET', '')


def instrument_info_callback(message):
    logger.debug(f"instrument_info_callback()")
    logger.info(message)
    pass


def orderbook_callback(message):
    logger.debug(f"orderbook_callback()")
    logger.info(message)
    pass


def position_callback(message):
    logger.debug(f"position_callback()")
    logger.info(message)


class HTTPTest(unittest.TestCase):

    @staticmethod
    def sleep_loop(loops=5, sleep_secs=1):
        i = 0
        while i < loops:
            i = i + 1
            sleep(sleep_secs)
            logger.info(f"Polling {i * sleep_secs}s out of {loops * sleep_secs}s")

    def test_instrument_info(self):
        # given
        usdt_public_ws = usdt_perpetual.PublicWebSocket("wss://stream.bybit.com/realtime_public")
        usdt_public_ws.custom_topic_stream("instrument_info.100ms.BTCUSDT", instrument_info_callback)

        # when then
        self.sleep_loop(5)
        usdt_public_ws.exit()

    def test_inverse_instrument_info(self):
        # given
        inverse_ws = inverse_perpetual.WebSocket("wss://stream.bybit.com/realtime")
        inverse_ws.custom_topic_stream("instrument_info.100ms.BTCUSD", instrument_info_callback)
        # when then
        self.sleep_loop(5)
        inverse_ws.exit()

    def test_position_callback(self):
        # given
        usdt_private_ws = usdt_perpetual.PrivateWebSocket("wss://stream-testnet.bybit.com/realtime_private",
                                                          api_key=API_KEY, api_secret=API_SECRET)
        usdt_private_ws.position_stream(position_callback)

        # when then
        self.sleep_loop(5, 2)
        usdt_private_ws.exit()
