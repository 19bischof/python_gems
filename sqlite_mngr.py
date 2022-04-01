import sqlite3
from typing import Iterable, Any
import prettytable
import pathlib


class sqlite3_functions:

    no_out = False

    def __init__(self, file_name="my_db.db"):
        self.file_path = pathlib.Path(
            __file__).parent.as_posix() + "/" + file_name

    @staticmethod
    def mng_conn(bosom):
        """connection context manager"""

        def ample(self, *args):
            with sqlite3.Connection(self.file_path) as conn:
                self.cursor = conn.cursor()
                bosom(self, *args)
                if self.no_out:
                    return
                if table_s := prettytable.from_db_cursor(self.cursor):
                    print(table_s)
        return ample

    def scrub(self, s):
        """prevents sql-injection when parametrizing tablenames"""
        new = ""
        assert isinstance(s, str)
        abc, nums, special = "abcdefghijklmnopqrstuvwxyz", "0123456789", "_ "
        for c in s.lower():
            if c in abc+nums+special:
                new += c
        return new

    @mng_conn
    def create_table(self, dirty_table_name: str, columns: Iterable[str]):
        """creates a table"""
        table_name = self.scrub(dirty_table_name)
        columns = list(columns)
        end_str = "("
        for c in columns:
            end_str += self.scrub(c) + ","
        end_str = end_str[:-1] + ");"
        query = f"CREATE TABLE IF NOT EXISTS {table_name} " + end_str
        self.cursor.execute(query)

    @mng_conn
    def drop(self, dirty_table_name: str):
        """drops a table"""
        table_name = self.scrub(dirty_table_name)
        query = f"""DROP TABLE IF EXISTS {table_name};"""
        self.cursor.execute(query)

    @mng_conn
    def describe(self, dirty_table_name: str):
        """describes table columns"""
        table_name = self.scrub(dirty_table_name)
        query = f"""PRAGMA table_info({table_name}); """
        self.cursor.execute(query)

    @mng_conn
    def select_all(self, dirty_table_name: str):
        """selects all columns from a table"""
        table_name = self.scrub(dirty_table_name)
        query = f"""SELECT rowid,* FROM {table_name};"""
        self.cursor.execute(query)

    @mng_conn
    def select_some(self, dirty_table_name: str, to_select: Iterable[str]):
        """selects some columns from a table"""
        table_name = self.scrub(dirty_table_name)
        cols = ",".join(to_select)
        query = "SELECT " + cols + f" FROM {table_name};"
        self.cursor.execute(query)

    @mng_conn
    def insert(self, dirty_table_name: str, values: Iterable[Any]):
        """inserts a row with values in a table"""
        table_name = self.scrub(dirty_table_name)
        params = ("?," * len(values))[:-1]
        query = f"INSERT INTO {table_name} VALUES (" + params + ");"
        self.cursor.execute(query, values)

    @mng_conn
    def update(self, dirty_table_name: str, set_str: str, where_str: str = ""):
        """updates rows in a table """
        table_name = self.scrub(dirty_table_name)
        if where_str != "":
            where_str = " WHERE " + where_str
        query = f"UPDATE {table_name} SET " + set_str + where_str + ";"
        self.cursor.execute(query)

    @mng_conn
    def print_tables(self):
        """prints the name of all tables"""
        query = """SELECT name FROM {}
        WHERE type ='table' 
        AND name NOT LIKE 'sqlite_%';"""
        try:
            self.cursor.execute(query.format("sqlite_schema"))
        except sqlite3.OperationalError:
            self.cursor.execute(query.format("sqlite_master"))

    @mng_conn
    def print_sqlite_version(self):
        """prints the sqlite version"""
        query = """SELECT sqlite_version();"""
        self.cursor.execute(query)

    @mng_conn
    def custom_query(self, query: str, params: Iterable[Any]):
        self.cursor(query, params)


if __name__ == "__main__":
    # example usage
    db = sqlite3_functions()
    db.no_out = False
    db.create_table("table2",("test text",))
    db.drop("table2")
    db.drop("table1")
    db.create_table("table1",("name text","age int"))
    db.print_tables()
    db.print_sqlite_version()
    db.describe("table1")
    db.select_all("table1")
    db.insert("table1",("herald",132))
    db.insert("table1",("hubert",120))
    db.select_some("table1",("name",))
    db.update("table1",'name = "hammer"',"name = 'hubert'")
    db.select_all("table1")
