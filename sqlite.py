import sqlite3


class Sqlite:
    """SQLite3のクラス
    """
    def __init__(self, db_path):
        """初期化

        Args:
            db_path: データベースファイルのパス
        """
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.curs = self.conn.cursor()

    def close_connect(self):
        """接続解除
        """
        self.conn.commit()
        self.curs.close()
        self.conn.close()
