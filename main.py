import eel

from bookmarks import bookmarks
import sqlite


db = sqlite.Sqlite('db.sqlite')

eel.init('web')


@eel.expose
def insert_bookmark(url, title, tag, description):
    result = bookmarks.insert_bookmark(db, url, title, tag, description)
    return result


@eel.expose
def get_bookmarks(url):
    if url == '':
        bs = bookmarks.get_bookmarks(db)
    else:
        bs = bookmarks.get_bookmarks(db, url)

    bs = [b for b in bs]

    return bs


@eel.expose
def update_bookmark(url, title, tag, description):
    bookmarks.update_bookmark(db, url, title, tag, description)


@eel.expose
def delete_bookmark(url):
    bookmarks.delete_bookmark(db, url)


bookmarks.create_table(db)
eel.start('templates/bookmarks.html', jinja_templates='templates')
