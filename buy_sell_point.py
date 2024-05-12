from os import listdir
from os.path import isfile, join
import logging
import concurrent.futures
import time
from stock_symbol import Symbol

def get_symbolfiles():
    symbol_path = "init_data"
    files = [join(symbol_path, f) for f in listdir(symbol_path) if isfile(join(symbol_path, f))]
    json_files = [f for f in files if f[-4:] == 'json']
    return json_files


def thread_function_track_symbol(symbol_file):
    logging.info("Thread %s: starting", symbol_file[0:-5])
    symbol = Symbol(symbol_file)
    symbol.track()
    logging.info("Thread %s: finishing", symbol_file[0:-5])


# start
if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    polling_interval = 1 * 60
    all_tracked_list = []

    while(True):
        updated_list = get_symbolfiles()
        new_tracked_files = [f for f in updated_list if f not in all_tracked_list]
        
        if len(new_tracked_files) > 0:
            with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
                executor.map(thread_function_track_symbol, new_tracked_files)

            all_tracked_list.append(new_tracked_files)

        time.sleep(polling_interval)
  