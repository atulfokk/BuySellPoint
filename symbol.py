"""This file provides actions and information about a stock symbol"""

from yahoo_fin import stock_info as si
import time
import datetime as dt
from notification import notification
from notification import Decision
import json as js


class Symbol():
    """This class defines a symbol. Tracks realtime price and notifies buy/sell points"""
    _default_sleep_duration = 15   # 15 minutes default waittime
    _day_start = dt.datetime.now()
    _day_end = dt.datetime.now()
    _notification_count = 0


    def __init__(self, symbol_file):
        self.symbol_file = symbol_file


    def __set_trading_day(self):
        """Sets the Currently running trading day. If it's past 5:30 PM or weekend, it sets the 
        next working day as trading day."""

        self._day_start = self._day_end = self.now
        self._day_start = self._day_start.replace(hour = 9)
        self._day_start = self._day_start.replace(minute = 0)
        self._day_start = self._day_start.replace(second = 0)
        self._day_end = self._day_end.replace(hour = 17)
        self._day_end = self._day_end.replace(minute = 30)
        self._day_end = self._day_end.replace(second = 0)
        
        if self.now > self._day_end:
            self._day_start += dt.timedelta(days=1)
            self._day_end += dt.timedelta(days=1)
        
        if self.now.weekday() > 4:
            self._day_start += dt.timedelta(days=7-self.now.weekday())
            self._day_end += dt.timedelta(days=7-self.now.weekday())
        
        if self._day_start.weekday() > 4:
            self._day_start += dt.timedelta(days=7-self._day_start.weekday())
            self._day_end += dt.timedelta(days=7-self._day_end.weekday())
    

    def track(self):
        """tracks the symbol price and notifies buy / sell"""
        self._notification_count = 0
        while (True):
            self.now = dt.datetime.now()
            self.__set_trading_day()
            try:
                with open(self.symbol_file) as fo:
                    self.symbol_info = js.load(fo)
            except FileNotFoundError:
                print(f'ERROR ({self.now}): File not Exist: {self.symbol_file}. Tracking will stop now.')
                return

            waittime = self.__wait_time_seconds()
            if waittime > 0:
                time.sleep(waittime)
                continue

            try:
                self.price = si.get_live_price(self.symbol_info['symbol'])

                if self.price <= float(self.symbol_info['buy_price']):
                    self.notify(self.symbol_info['buy_price'], Decision.Buy)
                elif self.price >= float(self.symbol_info['sell_price']):
                    self.notify(self.symbol_info['sell_price'], Decision.Sell)
                
                waittime = self._default_sleep_duration if self.symbol_info['interval'] == 'default' \
                        else int(self.symbol_info['interval'])
            except BaseException as err:
                print(f'ERROR ({self.now}) ({self.symbol_file}): {err=} {type(err)=}')

            time.sleep( waittime * 60)


    def __wait_time_seconds(self):
        """Find all the conditions if the tracking should not start yet."""
        # _day_start and _day_end must be updated before calling this
        # wait for night
        if self.symbol_info['dayNightDuration'] == 'dayTime':
            if self.now < self._day_start:
                self._notification_count = 0
                return (self._day_start - self.now).seconds

        waittime = self._default_sleep_duration if self.symbol_info['interval'] == 'default' \
                    else int(self.symbol_info['interval'])

        if self.symbol_info['notificationCount'] == '0':
            self._notification_count = 0
            return waittime * 60

        if not self.symbol_info['buy_price'] and not self.symbol_info['sell_price']:
            self._notification_count = 0
            return waittime * 60

        if self.symbol_info['notificationCount'] != 'default' and self._notification_count >= \
                int(self.symbol_info['notificationCount']):
            return waittime * 60

        return 0
    

    def notify(self, price_point, decision):
        message = notification(decision, self.symbol_info["symbol"], self.price, price_point)
        message.notify_on_windows()
        self._notification_count += 1