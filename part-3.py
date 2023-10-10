from flask import Flask, jsonify, request
from py3dbp import Packer, Bin, Item
from enum import Enum
from decimal import Decimal, getcontext

app = Flask(__name__)

class RotationType(Enum):
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"

def calculate_position(bin, items_packed, item):
    x = 0
    y = 0
    for packed_item in items_packed:
        x += packed_item['width']
        if x + item['width'] > bin.width:
            x = 0
            y += packed_item['height']
    
    return x, y

def calculate_remaining_volume(bin, items_packed):

    total_item_volume = sum(Decimal(item['volume']) for item in items_packed)
    remaining_volume = bin.get_volume() - total_item_volume
    return str(remaining_volume)

def pack_items_into_boxes(items, boxes):
    packer = Packer()
    unfitted_items = [] 

    for box in boxes:
        bin = Bin(box['name'], box['width'], box['height'], box['depth'], box['max_weight'])
        packer.add_bin(bin)

    packed_boxes = []

    for i in range(len(boxes)):
        bin = packer.bins[i]
        packed_box = {
            'box_name': bin.name,
            'box_width':bin.width,
            'box_height':bin.height,
            'box_number': i + 1,
            'max_weight': bin.max_weight,
            'remaining_volume': str(bin.get_volume()),
            'weight': 0,
            'items_packed': {}  
        }
        packed_boxes.append(packed_box)

    for item in items:
        for i in range(item['quantity']):
            item_name = str(item['name'])
            item_added = False
            for packed_box in packed_boxes:
                bin = packer.bins[packed_box['box_number'] - 1]
                item_volume = Decimal(item['width']) * Decimal(item['height']) * Decimal(item['depth'])
                if (bin.get_volume() >= item_volume and
                        packed_box['weight'] + item['weight'] <= packed_box['max_weight']):
                    if item_name in packed_box['items_packed']:
                        packed_box['items_packed'][item_name]['quantity'] += 1
                        packed_box['items_packed'][item_name]['volume'] += item_volume
                    else:
                        
                        x, y = calculate_position(bin, packed_box['items_packed'].values(), item)
                        
                        packed_item = {
                            'item_name': item_name,
                            'quantity': 1,
                            'volume': item_volume,
                            'rotation_type': item['rotation_type'],
                            'max_weight': item['weight'],
                            'width':item['width'],
                            'height':item['height'],
                            'x': x,
                            'y': y
                        }
                        packed_box['items_packed'][item_name] = packed_item
                    packed_box['remaining_volume'] = calculate_remaining_volume(bin, packed_box['items_packed'].values())
                    packed_box['weight'] += item['weight']
                    item_added = True
                    break

            if not item_added:
                unfitted_item = {
                    'item_name': item_name,
                    'quantity': 1,
                    'volume': item_volume,
                    'rotation_type': item['rotation_type'],
                    'max_weight' : item['weight'],
                    'width':item['width'],
                    'height':item['height']
                }
                unfitted_items.append(unfitted_item)

    return packed_boxes, unfitted_items



@app.route('/pack_boxes', methods=['POST'])
def allocate_boxes():
    data = request.get_json()

    items = data['items']
    boxes = data['boxes']

    packed_boxes, unfitted_items = pack_items_into_boxes(items, boxes)
    total_boxes = len(packed_boxes)

    return jsonify({'total_boxes': total_boxes, 'packed_boxes': packed_boxes, 'unfitted_items': unfitted_items})

if __name__ == '__main__':
    app.run(debug=True)