from flask import Flask, jsonify, request
from py3dbp import Packer, Bin, Item

app = Flask(__name__)

def pack_items_into_boxes(items, boxes):
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

    packer.pack()

    packed_data = []
    for i, box in enumerate(packer.bins):
        box_data = {
            'box_number': i + 1,
            'remaining_volume': box.get_volume() ,
            'weight': box.max_weight,
            'num_items': len(box.items),
            'items': []
        }
        for item in box.items:
            item_data = {
                'width': item.width,
                'height': item.height,
                'depth': item.depth,
                'max_weight': item.weight,
                'rotation_type': item.rotation_type,
                'position': item.position
            }
            box_data['items'].append(item_data)
        packed_data.append(box_data)

    return packed_data

@app.route('/allocate_boxes', methods=['POST'])
def allocate_boxes():
    data = request.get_json()

    items = data['items']
    boxes = data['boxes']

    packed_boxes = pack_items_into_boxes(items, boxes)

    total_boxes = len(packed_boxes)

    return jsonify({'total_boxes': total_boxes, 'packed_boxes': packed_boxes})

if __name__ == '__main__':
    app.run(debug=True)


