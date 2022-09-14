import typing
import aiosqlite

class AioTable:

    def __init__(self,
                 name: str,
                 db_path: str):
        self.name = name
        self.db_path = db_path

    @staticmethod
    def unpack_kwargs(*args, **kwargs):
        means = []
        parametrs = ""

        for mean in args:
            means.append(mean)

        for parametr in kwargs:
            means.append(kwargs[parametr])
            parametrs += f"{parametr}=?,"

        return means, parametrs[:-1]

    async def create(self, forced=False, **kwargs):
        if forced:
            await self.delete()
        sql_query = f"""CREATE TABLE IF NOT EXISTS {self.name}({("".join(f"{i} {kwargs[i]}," for i in kwargs))[:-1]})"""
        connection = aiosqlite.connect(self.db_path)
        async with connection.execute(sql_query) as cursor:
            return self

    async def delete(self):
        sql_query = f"""DROP {self.name}"""
        async with aiosqlite.connect(self.db_path).execute(sql_query) as cursor:
            return None

    async def insert(self, **kwargs):
        means, parametrs = self.unpack_kwargs(kwargs)

        parametrs.replace("=?", "")
        values = ("".join("?," for i in kwargs))[:-1]

        sql_query = f"""INSERT INTO TABLE {self.name}({parametrs}) values({values})"""
        async with aiosqlite.connect(self.db_path, means).execute(sql_query) as cursor:
            return None

    async def delete_row(self, **kwargs):
        means, parametrs = self.unpack_kwargs(kwargs)
        sql_query = f"""DELETE FROM {self.name} WHERE {parametrs}"""
        async with aiosqlite.connect(self.db_path, means).execute(sql_query) as cursor:
            return None

    async def get(self, column_name: str, **kwargs):
        means, parametrs = self.unpack_kwargs(kwargs)
        sql_query = f"""SELECT {column_name} FROM {self.name} WHERE {parametrs}"""
        async with aiosqlite.connect(self.db_path, means).execute(sql_query) as cursor:
            return await cursor.fetchone()

    async def set(self, column_name: str, column_mean: typing.Any, **kwargs):
        means, parametrs = self.unpack_kwargs(column_mean, kwargs)

        sql_query = f"""UPDATE {self.name} SET {column_name}=? WHERE {parametrs}"""

        async with aiosqlite.connect(self.db_path, means).execute(sql_query) as cursor:
            return None

    async def get_all(self):
        sql_query = f"""SELECT * FROM {self.name}"""
        async with aiosqlite.connect(self.db_path).execute(sql_query) as cursor:
            return await cursor.fetchall()

    async def __aiter__(self):
        return iter(await self.get_all())