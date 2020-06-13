from flask import Flask, render_template, send_file, request, redirect
import random
import main
import uuid
import pyqrcode

app = Flask(__name__)

@app.route('/')
def home():
    id = random.randint(1000,10000)
    hash = uuid.uuid4().hex
    id = str(id)
    # qrcode = pyqrcode.create('http://127.0.0.1:5001/get_in_queue/{}'.format(id))
    # qrcode.svg('uca-url.svg', scale=8)
    # qrcode.eps('uca-url.eps', scale=2)
    # qrcode.png('code.png', scale=6, module_color=[0, 0, 0, 128], background=[0xff, 0xff, 0xcc])
    # qrcode.show()
    return render_template('home.html', id=id)

@app.route('/create_queue/<id>', methods=['POST', 'GET'])
def create_queue(id):
    if request.method == 'POST':
        main.create_queue(id)
        id = 'Queue ID: {}'.format(main.check_id(id))
    
    if request.method == 'GET':
        id = main.check_id(id)
        if id is None:
            id = 'QUEUE ID DOESNT EXISTS'
        else:
            id = 'Queue ID: {}'.format(id)

    return render_template('create_queue.html', id=id)

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
        queue = main.get_queue(id)
        if not queue:
            queue = main.get_in_queue(id, name)
            position = main.get_position(id, name)
        else:
            position = main.get_position(id, name)
            if position is None:
                main.get_in_queue(id, name)
                position = main.get_position(id, name)

    return render_template('in_queue_id.html', position=position, id=id)

if __name__ == '__main__':
    app.run(debug=True, port=5001)