from flask import Flask, render_template, request, redirect
# from flask_sqlalchemy import SQLAlchemy
import random
#import main
import pyqrcode
import string
import time
import threading
import os

app = Flask(__name__)

data = {}
pop = []

@app.route('/')
def home():
    id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    # id = ''.join(random.choices(string.ascii_uppercase, k=6))
    return render_template('home.html', id=id)

@app.route('/admin/<id>', methods=['POST', 'GET'])
def admin(id):
    id = check_id(id)
    queue = ''
    if id is None:
        id = 'QUEUE ID DOESNT EXISTS'
        print(id)
    else:
        queue = get_queue(id)

    if request.method == 'POST':
        try:
            popped(queue[0])
            queue.pop(0)
        except:
            print("Queue is empty")
    
    try:
        now_serving = 'Now Serving: {}'. format(queue[0])
    except:
        now_serving = 'No Customers in line'
    try:
        next_cust = 'Next: {}'.format(queue[1])
    except:
        next_cust = ''

    return render_template('admin.html', id=id, queue=queue, now_serving=now_serving, next_cust=next_cust)

@app.route('/create_queue/<id>', methods=['POST', 'GET'])
def create_queue(id):

    qrcode = pyqrcode.create('http://127.0.0.1:5001/in_queue/id/{}'.format(id))
    qrcode.svg('uca-url.svg', scale=8)
    qrcode.eps('uca-url.eps', scale=2)
    qrcode.png('static/code{}.png'.format(id), scale=6, module_color=[0, 0, 0, 128], background=[0xFF,0xFF,0xFF])

    qr_pic = 'code{}.png'.format(id)
    num = id

    if request.method == 'POST':
        create_queue(id)
        id = '{}'.format(check_id(id))
    
    if request.method == 'GET':
        id = check_id(id)
        if id is None:
            id = 'QUEUE ID DOESNT EXISTS'
        else:
            id = '{}'.format(id)

    return render_template('create_queue.html', id=id, num=num, qr_pic=qr_pic)

@app.route('/get_in_queue')
def get_in_queue():
    return render_template('get_in_queue.html')

@app.route('/get_in_queue', methods=['POST'])
def get_id():
    id = request.form['id']
    id = check_id(id)
    if id is None:
        id = 'QUEUE ID DOESNT EXISTS'
    return id

@app.route('/in_queue', methods=['POST'])
def in_queue():
    id = get_id()
    return render_template('in_queue.html', id=id)

@app.route('/in_queue', methods=['POST'])
def get_name():
    name = request.form['name']
    return name

@app.route('/in_queue/id/<id>', methods=['POST', 'GET'])
def in_queue_id(id):
    position = 0
    if request.method == 'POST':
        name = get_name()
        queue = get_queue(id)
        if not queue:
            queue = get_in_queue(id, name)
            position = get_position(id, name)
        else:
            position = get_position(id, name)
            if position is None:
                get_in_queue(id, name)
                position = get_position(id, name)

        return redirect('/in_queue/id/{}/{}'.format(id, name))

    if request.method == 'GET':
        name = 'none'

    print("NAME: {}\n\n".format(name))

    del_pics()

    return render_template('in_queue_id.html', position=position, id=id, name=name)

@app.route('/in_queue/id/<id>/<name>')
def in_queue_name(id, name):
    id = check_id(id)
    pop = get_pop()
    print("POP", pop)
    if id is None:
        id = 'QUEUE ID DOESNT EXISTS'
    else:
        queue = get_queue(id)
        if not queue:
            queue = get_in_queue(id, name)
            position = get_position(id, name)
        if name in pop:
            position = 'out of line'
            remove(id, name)
        else:
            position = get_position(id, name)
            if position is None:
                get_in_queue(id, name)
                position = get_position(id, name)

    return render_template('in_queue_id.html', position=position, id=id, name=name)

@app.route('/news')
def news():
    return render_template('news.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')

def create_queue(id):
    print("creating queue")
    print("DATA:", data)
    queue = []
    data[id] = queue
    
def get_in_queue(id, name):
    print("getting in queue")
    print("DATA:", data)
    try:
        queue = data[id]
    except:
        return None
    
    queue.append(name)
    data[id] = queue
    return data[id]

def get_queue(id):
    print("getting queue")
    print("DATA:", data)
    try:
        if id in data:
            queue = data[id]
            return queue
        else:
            return None
    except:
        return None

def check_id(id):
    print("checking id")
    print("DATA:", data)
    try:
        if id in data:
            return id
        else:
            return None
    except:
        return None

def get_position(id, name):
    print("getting position")
    queue = data[id]
    count = 0
    for person in queue:
        count += 1
        if person == name:
            return count
    return None

def remove(id, name):
    queue = data[id]
    try:
        queue.remove(name)
    except:
        print("Item Already Removed")

def popped(name):
    print("POPPED\n\n")
    pop.append(name)

def get_pop():
    return pop

def clear_pop():
    pop.pop(0)
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

if __name__ == '__main__':
    app.run(host='127.0.0.1', threaded=True, debug=True, port=5001)
    