from arctic import CHUNK_STORE, Arctic

a = Arctic('localhost')


def get_store(db_name):
    a.initialize_library(db_name, lib_type=CHUNK_STORE)
    lib = a[db_name]
    return lib


def write_df(lib, code, df, chunk_size='M'):
    # lib = get_store(store)
    if code not in lib.list_symbols():
        lib.write(code, df, chunk_size=chunk_size)
    else:
        lib.update(code, df, chunk_size=chunk_size)
