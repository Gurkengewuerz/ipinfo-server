import sqlite3


class Database:
    def __init__(self, **kwargs):
        self.filename = kwargs.get('filename')

    def sql_do(self, sql, *params):
        self._db.execute(sql, params)
        self._db.commit()

    def retrieve(self, key):
        cursor = self._db.execute(key)
        return cursor

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, fn):
        self._filename = fn
        self._db = sqlite3.connect(fn)
        self._db.row_factory = sqlite3.Row

    @filename.deleter
    def filename(self):
        self.close()

    def close(self):
        self._db.close()
        del self._filename
