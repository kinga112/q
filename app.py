from flask import Flask, render_template, request, redirect
import random
import main
import pyqrcode
import string
import time
import threading
import os

app = Flask(__name__)


@app.route('/')
def home():
    id = ''.join(random.choices(string.ascii_uppercase, k=6))
    return render_template('home.html', id=id)

@app.route('/admin/<id>', methods=['POST', 'GET'])
def admin(id):
    id = main.check_id(id)
    queue = ''
    if id is None:
        id = 'QUEUE ID DOESNT EXISTS'
        print(id)
    else:
        queue = main.get_queue(id)

    print("QUEUE:", queue)
    names = queue.split(',')
    
    try:
        now_serving = 'Now Serving: {}'. format(names[0])
    except:
        now_serving = 'No Customers in line'
    try:
        next_cust = 'Next: {}'.format(names[1])
    except:
        next_cust = ''

    if request.method == 'POST':
        print("\nButton Pressed\n")
        main.remove(id, names[0])
        main.popped(names[0])

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
        main.create_queue(id)
        id = '{}'.format(main.check_id(id))
    
    if request.method == 'GET':
        id = main.check_id(id)
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
    id = main.check_id(id)
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
        main.get_in_queue(id, name)
        position = main.get_position(id, name)
        if position is None:
            main.get_in_queue(id, name)
            position = main.get_position(id, name)

        return redirect('/in_queue/id/{}/{}'.format(id, name))

    if request.method == 'GET':
        name = 'none'

    print("NAME: {}\n\n".format(name))

    main.del_pics()

    return render_template('in_queue_id.html', position=position, id=id, name=name)

@app.route('/in_queue/id/<id>/<name>')
def in_queue_name(id, name):
    position = 0
    id = main.check_id(id)
    pop = main.get_pop()
    if id is None:
        id = 'QUEUE ID DOESNT EXISTS'
    else:
        queue = main.get_queue(id)
        if queue is not None:
            position = main.get_position(id, name)
        if name in pop:
            position = 'out of line'
            main.remove(id, name)
            main.remove('pop', name)
        else:
            position = main.get_position(id, name)
            print("poposit:", position)
            if position is None:
                main.get_in_queue(id, name)
                position = main.get_position(id, name)

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
    
if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True, port=5001)
