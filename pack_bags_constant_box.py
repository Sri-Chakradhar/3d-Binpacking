from flask import Flask, jsonify, request
from itertools import permutations, combinations

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

def best_fit_3d(items, box_width, box_height, box_depth):
    boxes = [Box(box_width, box_height, box_depth)]

    for item in items:
        placed = False
        for box in boxes:
            if box.add_item(item):
                placed = True
                break
        
        if not placed:
            new_box = Box(box_width, box_height, box_depth)
            new_box.add_item(item)
            boxes.append(new_box)
    return boxes

def calculate_orientations(items, packed_boxes):
    orientations = {}
    levels = {}
    
    for box in packed_boxes:
        for item_index in box['item_order']:
            item = items[item_index]
            if item.orientation is not None:
                orientations[item_index] = item.orientation
            else:
                vertical_volume = item.height
                horizontal_volume = item.width 
                if vertical_volume >= horizontal_volume:
                    orientations[item_index] = 'vertical'
                else:
                    orientations[item_index] = 'horizontal'
            
            remaining_volume = box['remaining_volume']
            level = 1
            for placed_item_index in box['item_order']:
                placed_item = items[placed_item_index]
                remaining_volume -= placed_item.volume
                if remaining_volume < item.volume:
                    break
                level += 1
            levels[item_index] = level
    
    return orientations, levels

def total_ways(items, box_width, box_height, box_depth):
    box_volume = box_width * box_height * box_depth
    item_volumes = [item.width * item.height * item.depth for item in items]
    
    valid_item_combinations = []
    valid_item_permutations = []
    
    for r in range(1, len(items) + 1):
        item_combinations = combinations(item_volumes, r)
        for combo in item_combinations:
            if sum(combo) <= box_volume:
                valid_item_combinations.append(combo)
        
        item_permutations = permutations(item_volumes, r)
        for perm in item_permutations:
            if sum(perm) <= box_volume:
                valid_item_permutations.append(perm)
    
    return {
        'total_combinations': len(valid_item_combinations),
        'total_permutations': len(valid_item_permutations)
    }

@app.route('/pack_boxes', methods=['POST'])
def pack_boxes():
    data = request.get_json()

    items = []
    for item_data in data['items']:
        item = Item(
            item_data['width'], 
            item_data['height'], 
            item_data['depth'], 
            item_data['weight'],
            item_data.get('orientation')  
        )
        items.append(item)
    
    box_width = data['width']
    box_height = data['height']
    box_depth = data['depth']

    packed_boxes = best_fit_3d(items, box_width, box_height, box_depth)

    packed_data = []
    for i, box in enumerate(packed_boxes):
        box_data = {
            'box_number': i + 1,
            'remaining_volume': box.remaining_volume,
            'weight': box.weight,  
            'item_order': [items.index(item) for item in box.items],
            'num_items': len(box.items),
            'width': box.width,
            'height': box.height,
            'depth': box.depth,
            'items': []
        }
        
        for item_index in box_data['item_order']:
            item = items[item_index]
            item_data = {
                'width': item.width,
                'height': item.height,
                'depth': item.depth,
                'orientation': item.orientation,
                'weight': item.weight
            }
            box_data['items'].append(item_data)
        
        packed_data.append(box_data)

    orientations, levels = calculate_orientations(items, packed_data)
    
    total_way = total_ways(items, box_width, box_height, box_depth)

    total_boxes = len(packed_boxes)
    
    return jsonify({'total_boxes': total_boxes, 'packed_boxes': packed_data,'orientation':orientations,'level':levels,'total_ways':total_way})

if __name__ == '__main__':
    app.run(debug=True)