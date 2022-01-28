import json as js
import logging
import concurrent.futures
from turtle import title

from symbol import Symbol

def get_tracked_symbols():
    symbols_to_track = "init_data\TrackedSymbols.json"

    with open(symbols_to_track) as fo:
        list = js.load(fo)

    return [s for s in list if s['tracked'] == 'true']


def thread_function_track_symbol(symbol_node):
    logging.info("Thread %s: starting", symbol_node['symbol'])
    track = Symbol(symbol_node['symbol'])
    track.track(int(symbol_node['interval_minutes']), float(symbol_node['buy_price']), float(symbol_node['sell_price']))
    logging.info("Thread %s: finishing", symbol_node)


def is_interrupt():
    file = 'init_data\App.json'
    with open(file) as fo:
        config = js.load(fo)
    
    if config["interrupt_execution"] == "true":
        return True
    else:
        return False


tracked_list = get_tracked_symbols()


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(thread_function_track_symbol, tracked_list)

