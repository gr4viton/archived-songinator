from flask import request, url_for, g
from flask_api import FlaskAPI, status, exceptions

import sqlite3

app = FlaskAPI(__name__)

db = 'database.db'


notes = {
    0: 'do the shopping',
    1: 'build the codez',
    2: 'paint the door',
}

def note_repr(key, db_saved=True):
    data = {
        'url': request.host_url.rstrip('/') + url_for('notes_detail', key=key),
        'text': notes[key]
    }
    if not db_saved:
        data['db_saved'] = db_saved
    return data


@app.route("/", methods=['GET', 'POST'])
def notes_list():
    """
    List or create notes.
    """
    if request.method == 'POST':
        note = str(request.data.get('text', ''))
        idx = max(notes.keys()) + 1
        notes[idx] = note
        return note_repr(idx), status.HTTP_201_CREATED

    # request.method == 'GET'
    return [note_repr(idx) for idx in sorted(notes.keys())]


#def query_db(f):
#    def wrapper(f):
#
#        conn = sqlite3.connect(db)
#        c = conn.cursor()
#        c.execute(text)
#        conn.close()
#    return wrapper

# decorators with
# def query_db_dec(argument):
#    def real_decorator(function):
#        def wrapper(*args, **kwargs):
#            funny_stuff()
#            something_with_argument(argument)
#            function(*args, **kwargs)
#            more_funny_stuff()
#        return wrapper
#    return real_decorator

def create_table():
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute('''create table if not exists name
             (key text, note text)''')
    conn.close()


def add_to_db(key, note):
    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute("INSERT INTO notes VALUES ('", str(key), "','", str(note), "')")

        conn.commit()
        conn.close()
        return True
    except Exception as ex:
        return ex


def get_from_db(key):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("SELECT * FROM notes WHERE symbol=?)", key)
    ret = c.fetchone()
    conn.commit()
    conn.close()
    print(ret)
    return


@app.route("/<int:key>/", methods=['GET', 'PUT', 'DELETE'])
def notes_detail(key):
    """
    Retrieve, update or delete note instances.
    """
    if request.method == 'PUT':
        #return {'data': request.data}
        note = str(request.data.get('text', ''))

        notes[key] = note
        ex = add_to_db(key, note)
        db_saved = ex is True
        return note_repr(key, db_saved)

    elif request.method == 'DELETE':
        notes.pop(key, None)
        return '', status.HTTP_204_NO_CONTENT

    # request.method == 'GET'
    if key not in notes:
        get_from_db(key)
        raise exceptions.NotFound()
    return note_repr(key)


if __name__ == "__main__":
    create_table()
    app.run(debug=True)
