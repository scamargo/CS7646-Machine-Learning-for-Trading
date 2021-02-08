import os
import pandas as pd
import numpy as np

def symbol_to_path(symbol, base_dir="data"):
    return os.path.join(base_dir,"{}.csv".format(str(symbol)))

def get_max_index(a):
    return np.argmax(a)

def test_run():
    a = np.array([9,6,2,3,12,14,7,10],dtype=np.int32)
    print("Array: {}".format(a))

    print("Max value: {}".format(a.max()))
    print("Max index: {}".format(get_max_index(a)))

if __name__ == "__main__":
    test_run()
    


