import sqlite3
import os
from src.server.database import errors


class DbManager:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def connect_db(self) -> tuple[sqlite3.Connection, sqlite3.Cursor]:
        connect = sqlite3.connect(self.db_path)
        cursor = connect.cursor()

        return connect, cursor

    def create_db(self, create_script: str) -> None:
        if not os.path.exists(self.db_path):
            self.execute_sql_script(create_script)

    def execute_sql_script(self, script: str) -> None:
        connect, cursor = self.connect_db()

        if not os.path.exists(script):
            raise errors.MissedScript

        cursor.executescript(open(script).read())
        connect.commit()
        connect.close()

    def execute_query(self, query: str, fetchone: bool = True, args: tuple = None):
        connect, cursor = self.connect_db()

        try:
            if fetchone:
                res = connect.execute(query, args).fetchone()
            else:
                res = cursor.execute(query).fetchall()
        except sqlite3.IntegrityError:
            connect.close()
            return {'error': 'request contains unique error'}

        connect.commit()
        connect.close()
        return res
