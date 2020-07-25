import threading
import os

data = {}
pop = []

def create_queue(id):
    print("creating queue")
    queue = []
    data[id] = queue
    
def get_in_queue(id, name):
    print("getting in queue")
    try:
        queue = data[id]
    except:
        return None
    
    queue.append(name)
    data[id] = queue
    return data[id]

def get_queue(id):
    print("getting queue")
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
