import pandas as pd

data = {}

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
