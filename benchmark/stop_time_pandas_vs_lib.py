import pandas as pd
from src.collection import Collection
from custom_dataclasses.stop_times import StopTimes
import timeit


def pandas_exec():
    df = pd.read_csv('data/stop_times.csv')
    return df['stop_sequence']

def lib_exec():
    c = Collection(["data", "stop_times.csv"], StopTimes)
    return c.select(StopTimes.stop_sequence)

def lib_exec_collect():
    c = Collection(["data", "stop_times.csv"], StopTimes)
    return c.select(StopTimes.stop_sequence).collect()


if __name__ == '__main__':
    print('Pandas:', timeit.timeit(pandas_exec, number=1))
    print('Lib:', timeit.timeit(lib_exec, number=1))
    print('Lib collect', timeit.timeit(lib_exec_collect, number=1))