""" This module contains features to notify a content on windows and android"""
import enum
from plyer import notification as windows_notification

Decision = enum.Enum('Decision', 'Buy Sell')

class notification():
    """This class defines a notification of buy or sell type decision"""

    _timeout = 20

    def __init__(self, decision, symbol, current_price, price_point):
        self.decision = decision
        self.symbol = symbol
        self.current_price = current_price
        self.price_point = price_point
    

    def notify_on_windows(self):
        windows_notification.notify(
            title = f'{self.decision.name} {self.symbol.title()}',
            message = f'Current price {self.current_price} reached or crossed {self.decision.name} point {self.price_point}.',
            app_icon = 'resources\photo_frame_picture_wall_icon_209724.ico',
            timeout = self._timeout
            )
