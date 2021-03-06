from storage.kv_store_rocksdb import KeyValueStorageRocksdb

try:
    import rocksdb
except ImportError:
    print('Cannot import rocksdb, please install')


class IntegerComparator(rocksdb.IComparator):
    def compare(self, a, b):
        a = int(a)
        b = int(b)
        return a - b

    def name(self):
        return b'IntegerComparator'


class KeyValueStorageRocksdbIntKeys(KeyValueStorageRocksdb):
    def __init__(self, db_dir, db_name, open=True):
        super().__init__(db_dir, db_name, open)

    def open(self):
        opts = rocksdb.Options()
        opts.create_if_missing = True
        opts.comparator = IntegerComparator()
        self._db = rocksdb.DB(self._db_path, opts)

    def get_equal_or_prev(self, key):
        # return value can be:
        #    None, if required key less then minimal key from DB
        #    Equal by key if key exist in DB
        #    Previous if key does not exist in Db, but there is key less than required

        key = self.to_byte_repr(key)
        itr = self._db.itervalues()
        itr.seek_for_prev(key)
        try:
            value = next(itr)
        except StopIteration:
            value = None
        return value
