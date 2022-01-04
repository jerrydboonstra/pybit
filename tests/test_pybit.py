import time
import unittest

from pybit import HTTP

http = HTTP('https://api.bybit.com')


class HTTPTest(unittest.TestCase):

    def test_orderbook(self):
        self.assertEqual(
            http.orderbook(symbol='BTCUSD')['ret_msg'],
            'OK'
        )

    def test_query_kline(self):
        self.assertEqual((http.query_kline(symbol='BTCUSD', interval='1',
                                           from_time=int(time.time()) - 60 * 60)['ret_msg']), 'OK')

    def test_latest_information_for_symbol(self):
        self.assertEqual(http.latest_information_for_symbol()['ret_msg'], 'OK')

    def test_public_trading_records(self):
        self.assertEqual(http.public_trading_records(symbol='BTCUSD')['ret_msg'], 'OK')

    def test_query_symbol(self):
        self.assertEqual(http.query_symbol()['ret_msg'], 'OK')

    def test_server_time(self):
        self.assertEqual(http.server_time()['ret_msg'], 'OK')

    def test_announcement(self):
        self.assertEqual(http.announcement()['ret_msg'], 'OK')

    # We can't really test authenticated endpoints without keys, but we
    # can make sure it raises a PermissionError.
    def test_place_active_order(self):
        with self.assertRaises(PermissionError):
            http.place_active_order(symbol='BTCUSD', order_type='Market', side='Buy', qty=1)
