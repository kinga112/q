import threading
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv('.env.local')
uri = os.getenv('POSTGRES_URL')
conn = psycopg2.connect(uri)
cursor = conn.cursor()

def create_queue(id):
    try:
        create = "CREATE TABLE {} (id serial primary key, name varchar(256));".format(id)
        conn = psycopg2.connect(uri)
        cursor = conn.cursor()
        cursor.execute(create)
        conn.commit()
    except:
        cursor.execute("ROLLBACK")
        conn.commit()
        print("Table [{}] already created".format(id))
    try:
        pop = "CREATE TABLE pop{} (id serial primary key, name varchar(256));".format(id)
        cursor.execute(pop)
        conn.commit()
    except:
        cursor.execute("ROLLBACK")
        conn.commit()
        print("Table [pop{}] already created".format(id))
    
def get_in_queue(id, name):
    print("NAME 0: ", name)
    if '%' in name:
        return
    try:
        conn = psycopg2.connect(uri)
        cursor = conn.cursor()
        get = "SELECT * FROM {}".format(id)
        cursor.execute(get)
        for row in cursor:
            print("ROWROWRORW: ", row)
            if name in row.replace(' ', '.'):
                print(cursor)
                return
        else:
            print('nah man')
    except:
        print('Error ')
    try:
        conn = psycopg2.connect(uri)
        cursor = conn.cursor()
        insert = "INSERT into {} (name) values ('{}');".format(id, name.replace(' ', '.'))
        cursor.execute(insert)
        conn.commit()
    except:
        cursor.execute("ROLLBACK")
        conn.commit()
        print("Error: [get_in_queue]")

def get_queue(id):
    try:
        conn = psycopg2.connect(uri)
        cursor = conn.cursor()
        get = "SELECT * FROM {}".format(id)
        cursor.execute(get)
        queue = []
        for row in cursor:
            queue.append(row[1])
        return queue
    except:
        cursor.execute("ROLLBACK")
        conn.commit()
        print("Error: [get_queue]")
        return None

def check_id(id):
    try:
        conn = psycopg2.connect(uri)
        cursor = conn.cursor()
        get = "SELECT * FROM {}".format(id)
        print("GET: {}".format(get))
        cursor.execute(get)
        return id
    except:
        cursor.execute("ROLLBACK")
        conn.commit()
        print("Error: [check_id]")
        return None

def get_position(id, name):
    try:
        conn = psycopg2.connect(uri)
        cursor = conn.cursor()
        get = "SELECT * FROM {}".format(id)
        cursor.execute(get)
        count = 0
        for row in cursor:
            count += 1
            if str(row[1]) == name:
                return count
    except:
        cursor.execute("ROLLBACK")
        conn.commit()
        print("Error: [get_position]")
        return None

def remove(id, name):
    print("NAME 1: ", name)
    try:
        conn = psycopg2.connect(uri)
        cursor = conn.cursor()
        delete = "DELETE FROM {} Where name = '{}';".format(id, name)
        cursor.execute(delete)
        conn.commit()
        get = "SELECT * FROM {}".format(id)
        cursor.execute(get)
        queue = []
        for row in cursor:
            queue.append(row[1])
        return queue
    except:
        cursor.execute("ROLLBACK")
        conn.commit()
        print("Error: [remove]")

def popped(id, name):
    print("NAME 2: ", name)
    print('popped')
    try:
        conn = psycopg2.connect(uri)
        cursor = conn.cursor()
        insert = "INSERT into pop{} (name) values ('{}');".format(id, name)
        cursor.execute(insert)
        conn.commit()
    except:
        cursor.execute("ROLLBACK")
        conn.commit()
        print("Error: [popped]")

def get_pop(id):
    try:
        conn = psycopg2.connect(uri)
        cursor = conn.cursor()
        get = "SELECT * FROM pop{}".format(id)
        cursor.execute(get)
        data = ''
        for row in cursor:
            data += row[1]
        return data
    except:
        cursor.execute("ROLLBACK")
        conn.commit()
        print("Error: [get_pop]")
        return None

def del_pics():
    folder_path = '/tmp/'
    folder = os.listdir(folder_path)

    for images in folder:
        if images.__contains__("code"):
            os.remove(os.path.join(folder_path, images))

    timer = threading.Timer(60, del_pics)
    timer.start()
