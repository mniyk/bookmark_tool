import datetime

import requests
from bs4 import BeautifulSoup


def create_table(db):
    sql = '''
            CREATE TABLE IF NOT EXISTS bookmarks(
                url TEXT, title TEXT, tag TEXT, description TEXT, created_at TEXT
            );
        '''
    db.curs.execute(sql)


def get_bookmarks(db, url=None):
    sql = 'SELECT * FROM bookmarks'

    if url:
        sql = f'{sql} WHERE url="{url}"'

    sql = sql + ';'

    db.curs.execute(sql)
    bs = [[b[0], b[1], b[2], b[3], b[4]] for b in db.curs.fetchall()]

    return bs


def insert_bookmark(db, url, title, tag, description):
    sql = f'SELECT 1 FROM bookmarks WHERE url="{url}";'

    db.curs.execute(sql)

    if db.curs.fetchone():
        return False
    else:
        if title == '':
            try:
                request = requests.get(url)
                soup = BeautifulSoup(request.text, 'html.parser')
                title = soup.title.text
            except:
                return False

        sql = f'''
                INSERT INTO bookmarks VALUES (
                    "{url}", "{title}", "{tag}", "{description}", "{str(datetime.datetime.now())}"
                );
            '''
        db.curs.execute(sql)
        db.conn.commit()
        return True


def update_bookmark(db, url, title, tag, description):
    sql = f'''
        UPDATE bookmarks
        SET title="{title}", tag="{tag}", description="{description}"
        WHERE url="{url}";
    '''
    db.curs.execute(sql)
    db.conn.commit()


def delete_bookmark(db, url):
    sql = f'DELETE FROM bookmarks WHERE url="{url}";'
    db.curs.execute(sql)
    db.conn.commit()
