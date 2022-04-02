import sqlite3
from typing import Iterable, Any, List, Tuple
import prettytable
import pathlib


class quick_lite3:
    """Simple functions to quickstart your sqlite3 database.
    Extensible with custom_query() or inheriting this class and 
    implementing your own functions. 
    Important: If you do, decorate your functions with '@quick_lite3.mng_conn' !"""
    print_output = True

    def __init__(self, file_name="my_db.db"):
        self.file_path = pathlib.Path(
            __file__).parent.as_posix() + "/" + file_name
        self.conn = sqlite3.Connection(self.file_path)

    def mng_conn(bosom) -> List[Tuple]|None:
        """Decorater - Manages Transactions and prints output if self.print_output
        :return: The cursor data
        """

        def ample(self, *args):
            with self.conn:
                self.cursor = self.conn.cursor()
                bosom(self, *args)
            curs_like = self.pseudo_cursor()
            if self.print_output:
                if table_s := prettytable.from_db_cursor(curs_like):
                    print(table_s)
            return curs_like.body
        return ample

    def pseudo_cursor(self):
        """Create Cursor-like Object for prettytable"""
        class _:
            def __init__(soul):
                soul.body = self.cursor.fetchall()
                soul.description = self.cursor.description

            def fetchall(soul):
                return soul.body
        return _()

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
    db = quick_lite3()
    db.print_output = True
    db.create_table("table2", ("test text",))
    db.drop("table2")
    db.drop("table1")
    db.create_table("table1", ("name text", "age int"))
    db.print_tables()
    db.print_sqlite_version()
    db.describe("table1")
    db.select_all("table1")
    db.insert("table1", ("herald", 132))
    db.insert("table1", ("hubert", 120))
    db.select_some("table1", ("name",))
    db.update("table1", 'name = "hammer"', "name = 'hubert'")
    db.select_all("table1")

    class test(quick_lite3):
        @quick_lite3.mng_conn
        def test(self):
            query = """SELECT sqlite_version();"""
            self.cursor.execute(query)
    t = test()
    t.test()
