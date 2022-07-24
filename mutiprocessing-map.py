from multiprocessing import Pool
from random import random
import time
import os


def func(i):
    rdm_time = random() * 1000
    time.sleep(rdm_time)
    print(f"{i} slept for {rdm_time}")

pool = Pool(os.cpu_count())
pool.map(func, range(30))
pool.close()
pool.join()
