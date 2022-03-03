import sqlite3

def connect():
    conn = sqlite3.connect('events.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS event (Id INTEGER PRIMARY KEY , date text , appliance text , "
                "active_energy float, reactive_energy float, timestamp text , state integer)")
    conn.commit()
    conn.close()
    print('Database Created')


def insert(date , appliance , active_energy , reactive_energy , timestamp , state):
    conn = sqlite3.connect('events.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO event VALUES (NULL , ?,?,?,?,?,?)" , (date , appliance , active_energy ,
                                                                     reactive_energy , timestamp , state))
    conn.commit()
    conn.close()
    print('Event created')

def view():
    conn = sqlite3.connect('events.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM event")
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows

def delete(id):
    conn = sqlite3.connect('events.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM event WHERE id=? ", (id,))
    conn.commit()
    conn.close()
    print('Event deleted')

def search(date='' , appliance='' , active_energy='' , reactive_energy='' , timestamp='' , state=''):
    conn = sqlite3.connect('events.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM event WHERE date=?  OR appliance=? OR active_energy=? OR reactive_energy=? OR timestamp=?"
                " OR state=?" ,
                (date , appliance , active_energy , reactive_energy , timestamp , state))
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows

connect()
