import sqlite3
import typing

class Connection:
    def __init__(self, db_path):
        self.db_path = db_path
        self.__connection: sqlite3.Connection = None
        self.__cursor: sqlite3.Cursor = None

    def __enter__(self):
        self.__connection = sqlite3.connect(self.db_path)
        self.__cursor = self.__connection.cursor()
        return self.__cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__cursor.close()
        self.__connection.commit()
        self.__connection.close()

class Table:

    def __init__(self,
                 name: str,
                 db_path: str):
        self.name = name
        self.db_path = db_path

    @staticmethod
    def unpack_kwargs(kwargs: dict, *args):
        means = []
        parametrs = ""
        for mean in args:
            means.append(mean)
        for parametr in kwargs:
            means.append(kwargs[parametr])
            parametrs += f"{parametr}=?,"
        return means, parametrs[:-1]

    def create(self, forced=False, **kwargs):
        if forced:
            self.delete()
        sql_query = f"""CREATE TABLE IF NOT EXISTS {self.name}({("".join(f"{i} {kwargs[i]}," for i in kwargs))[:-1]})"""
        with Connection(self.db_path) as cur:
            cur.execute(sql_query)
        return self

    def delete(self):
        sql_query = f"""DROP {self.name}"""
        with Connection(self.db_path) as cur:
            cur.execute(sql_query)

    def insert(self, **kwargs):
        means, parametrs = self.unpack_kwargs(kwargs)
        values = ("".join("?," for i in kwargs))[:-1]
        sql_query = f"""INSERT INTO {self.name}({parametrs}) values({values})""".replace("=?", "")
        with Connection(self.db_path) as cur:
            cur.execute(sql_query, means)

    def delete_row(self, **kwargs):
        means, parametrs = self.unpack_kwargs(kwargs)
        sql_query = f"""DELETE FROM {self.name} WHERE {parametrs}"""
        with Connection(self.db_path) as cur:
            cur.execute(sql_query, means)

    def get(self, column_name: str, **kwargs):
        means, parametrs = self.unpack_kwargs(kwargs)
        sql_query = f"""SELECT {column_name} FROM {self.name} WHERE {parametrs}"""
        with Connection(self.db_path) as cur:
            result = cur.execute(sql_query, means).fetchall()
        return result

    def set(self, column_name: str, column_mean: typing.Any, **kwargs):
        means, parametrs = self.unpack_kwargs(column_mean, kwargs)
        sql_query = f"""UPDATE {self.name} SET {column_name}=? WHERE {parametrs}"""
        with Connection(self.db_path) as cur:
            cur.execute(sql_query, means)

    def get_all(self):
        sql_query = f"""SELECT * FROM {self.name}"""
        with Connection(self.db_path) as cur:
            result = cur.execute(sql_query).fetchall()
        return result

    def __iter__(self):
        return iter(self.get_all())

    def __len__(self):
        return len(self.get_all())