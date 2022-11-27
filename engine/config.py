from pathlib import Path

DATA_DIR = Path(__file__).parent.parent.joinpath("data")

DATA_DIR_HDF5 = DATA_DIR.joinpath('hdf5')
DATA_DIR_HDF5_ALL = DATA_DIR_HDF5.joinpath('all.h5')
DATA_DIR_HDF5_CACHE = DATA_DIR_HDF5.joinpath('cache.h5')

DATA_DIR_CSV = DATA_DIR.joinpath('csv')
DATA_DIR_BKT_RESULT = DATA_DIR.joinpath('bkt_result')

dirs = [DATA_DIR, DATA_DIR_CSV, DATA_DIR_BKT_RESULT]
for dir in dirs:
    dir.mkdir(exist_ok=True, parents=True)


