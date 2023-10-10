from flask import Flask,jsonify,request
from py3dbp import Packer, Bin, Item

app = Flask(__name__)

class Box:
    def __init__(self, width, height, depth):
        self.width = width
        self.height = height
        self.depth = depth
        self.remaining_volume = width * height * depth
        self.items = []
        self.weight = 0

    def add_item(self, item):
        if self.remaining_volume >= item.volume:
            self.items.append(item)
            self.remaining_volume -= item.volume
            self.weight += item.weight
            return True
        return False

class Item:
    def __init__(self, width, height, depth, weight, orientation=None):
        self.width = width
        self.height = height
        self.depth = depth
        self.weight = weight
        self.orientation = orientation
        self.volume = width * height * depth


def pack_boxes(items, boxes):
    packer = Packer()

    for box in boxes:
        bin = Bin(box['name'],box['width'], box['height'], box['depth'], box['max_weight'])
        packer.add_bin(bin)
        print(box)

    print("         -------------------         ")

    for item in items:
        object = Item(item['name'],item['width'], item['height'], item['depth'], item['weight'])
        packer.add_item(object)
        print(item)

    boxes.sort(
            key=lambda bin: bin.get_volume(), reverse=False
        )
    items.sort(
            key=lambda item: item.get_volume(), reverse=False
        )


@app.route('/pack_box',methods=['POST'])
def pack_the_boxes():

    
    return

if __name__ == '__main__':
    app.run(debug=True)