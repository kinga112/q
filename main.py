import threading
import os
import psycopg2

uri = 'postgres://postgres:kinga112@127.0.0.1:5432'
# uri = os.environ['DATABASE_URL']
conn = psycopg2.connect(uri)
cursor = conn.cursor()

try:
    pop = "CREATE TABLE pop (id serial primary key, name varchar(256));"
    cursor.execute(pop)
    conn.commit()
except:
    cursor.execute("ROLLBACK")
    conn.commit()
    print("Table [pop] already created")

def create_queue(id):
    try:
        create = "CREATE TABLE {} (id serial primary key, name varchar(256));".format(id)
        cursor.execute(create)
        conn.commit()
    except:
        cursor.execute("ROLLBACK")
        conn.commit()
        print("Table [{}] already craeted".format(id))
    
def get_in_queue(id, name):
    try:
        insert = "INSERT into {} (name) values ('{}');".format(id, name)
        cursor.execute(insert)
        conn.commit()
    except:
        cursor.execute("ROLLBACK")
        conn.commit()
        print("Error: [get_in_queue]")

def get_queue(id):
    try:
        get = "SELECT * FROM {}".format(id)
        cursor.execute(get)
        queue = ''
        for row in cursor:
            queue = queue + '{}, '.format(row[1])
        queue = queue[0:-2]
        return queue
    except:
        cursor.execute("ROLLBACK")
        conn.commit()
        print("Error: [get_queue]")
        return None

def check_id(id):
    try:
        get = "SELECT * FROM {}".format(id)
        cursor.execute(get)
        return id
    except:
        cursor.execute("ROLLBACK")
        conn.commit()
        print("Error: [check_id]")
        return None

def get_position(id, name):
    try:
        get = "SELECT * FROM {}".format(id)
        cursor.execute(get)
        count = 0
        for row in cursor:
            count += 1
            name1 = row[1]
            if name1 == name:
                return count
    except:
        cursor.execute("ROLLBACK")
        conn.commit()
        print("Error: [get_position]")
        return None

def remove(id, name):
    try:
        delete = "DELETE FROM {} Where name = '{}';".format(id, name)
        cursor.execute(delete)
        conn.commit()
    except:
        cursor.execute("ROLLBACK")
        conn.commit()
        print("Error: [remove]")

def pop_remove(id):
    try:
        delete = "DELETE FROM {} LIMIT 1;"
        cursor.execute(delete)
        conn.commit()
    except:
        cursor.execute("ROLLBACK")
        conn.commit()
        print("Error: [pop_remove]")

def popped(name):
    insert = "INSERT into pop (name) values ('{}');".format(name)
    cursor.execute(insert)
    conn.commit()

def get_pop():
    get = "SELECT * FROM pop"
    cursor.execute(get)
    data = ''
    for row in cursor:
        data += row[1]
    return data

def clear_pop():
    drop = "DROP pop"
    cursor.execute(drop)
    conn.commit()
    timer = threading.Timer(10, clear_pop)
    timer.start()

def del_pics():
    folder_path = 'static/'
    folder = os.listdir(folder_path)

    for images in folder:
        if images.__contains__("code"):
            os.remove(os.path.join(folder_path, images))

    timer = threading.Timer(60, del_pics)
    timer.start()
