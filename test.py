import os.path
import pandas as pd
from main import *
import time
import multiprocessing.pool

if __name__ == '__main__':
    #
    start_time = time.time()
    #

    db = Database()
    df = db.check_exist('H:\\Zdjęcia\\D7200')

    print(os.path.curdir)

    #
    end_time = time.time()
    print((end_time - start_time) * 1000, 'ms')
    #
