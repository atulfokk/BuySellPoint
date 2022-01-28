"""This file provides actions and information about a symbol"""

from yahoo_fin import stock_info as si
import time
from plyer import notification

class Symbol():
    """This class defines a symbol. Tracks realtime price and notifies buy/sell points"""
    def __init__(self, symbol_name):
        self.name = symbol_name
        self.stop_tracking = "false"
    
    def track(self, duration_minutes, buy_price, sell_price):
        """tracks the symbol price and notifies buy / sell"""
        while (self.stop_tracking == 'false'):
            self.price = si.get_live_price(self.name)

            if self.price <= buy_price:
                self.notify(buy_price, 'buy')
            elif self.price >= sell_price:
                self.notify(sell_price, 'sell')
            
            time.sleep(60 * int(duration_minutes))


    def stop_tracking(self):
        self.stop_tracking = "true"
    

    def notify(self, price_point, decision):
        notification.notify(
            title = f'{decision.title()} {self.name.title()}',
            message = f'Current price {self.price} reached or crossed {decision} point {price_point}.',
            app_icon = 'resources\photo_frame_picture_wall_icon_209724.ico',
            timeout = 10,
)