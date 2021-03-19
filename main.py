import datetime
import eel
from sqlite import Sqlite


db_path = 'db.sqlite'
db = Sqlite(db_path)


def create_table():
    sql = '''
        CREATE TABLE IF NOT EXISTS bookmark(
            title TEXT, tag TEXT, url TEXT, description TEXT, 
            created_at TEXT, updated_at TEXT
        );
    '''
    db.curs.execute(sql)


@eel.expose
def get_bookmark():
    sql = 'SELECT title, tag, url FROM bookmark;'
    db.curs.execute(sql)
    bookmarks = db.curs.fetchall()

    return bookmarks


@eel.expose
def detail_bookmark(url):
    sql = f"SELECT title, tag, url, description FROM bookmark WHERE url='{url}';"
    db.curs.execute(sql)
    bookmarks = db.curs.fetchone()

    return bookmarks


@eel.expose
def delete_bookmark(url):
    sql = f"DELETE FROM bookmark WHERE url='{url}';"
    db.curs.execute(sql)
    db.conn.commit()


@eel.expose
def update_bookmark(title, tag, url, description):
    sql = f"""
        UPDATE bookmark 
        SET title='{title}', tag='{tag}', url='{url}', description='{description}' 
        WHERE url='{url}';
    """
    db.curs.execute(sql)
    db.conn.commit()


@eel.expose
def add_bookmark(title, tag, url, description):
    sql = f"SELECT 1 FROM bookmark WHERE url='{url}';"

    db.curs.execute(sql)

    if db.curs.fetchone():
        return False
    else:
        sql = f"""
            INSERT INTO bookmark
            VALUES (
                '{title}', '{tag}', '{url}', '{description}',
                '{str(datetime.datetime.now())}', '{str(datetime.datetime.now())}'
            );
        """
        db.curs.execute(sql)
        db.conn.commit()

        return True


create_table()

eel.init('web')
eel.start('index.html', size=(600, 400))
