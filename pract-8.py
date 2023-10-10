from flask import Flask, request, jsonify

app = Flask(__name__)

class Box:
    def __init__(self, boxno, width, height, depth, capacity):
        self.boxno = boxno
        self.width = width
        self.height = height
        self.depth = depth
        self.capacity = capacity
        self.remaining_volume = width * height * depth
        self.items = []
        self.boxused = 0
        self.itemsinbox = []

    def add_item(self, item):
        if self.remaining_volume >= item.volume and not item.occupied:
            self.items.append(item)
            self.remaining_volume -= item.volume
            item.occupied = True
            self.itemsinbox.append(item.name)
            self.boxused += 1
            return True
        return False

class Item:
    def __init__(self, name, width, height, depth, weight, quantity, orientation=None):
        self.name = name
        self.width = width
        self.height = height
        self.depth = depth
        self.weight = weight
        self.orientation = orientation
        self.volume = width * height * depth
        self.occupied = False
        self.quantity = quantity

@app.route('/pack', methods=['POST'])
def pack_items():
    data = request.get_json()

    typeofitems = data.get('typeofitems')
    typeofbins = data.get('typeofbins')
    items_data = data.get('items')
    bins_data = data.get('bins')

    items = []
    for item_data in items_data:
        item = Item(
            name=item_data['name'],
            width=item_data['width'],
            height=item_data['height'],
            depth=item_data['depth'],
            weight=item_data['weight'],
            quantity=item_data.get('quantity', 1)  # Default to 1 if quantity is not specified
        )
        items.append(item)

    bins = []
    for bin_data in bins_data:
        box = Box(
            boxno=bin_data['boxno'],
            width=bin_data['width'],
            height=bin_data['height'],
            depth=bin_data['depth'],
            capacity=bin_data['capacity'],
        )
        bins.append(box)

    items.sort(key=lambda item: item.volume, reverse=True)

    for item in items:
        packed = 0
        for box in bins:
            if box.remaining_volume >= item.volume and not item.occupied and packed < item.quantity:
                if box.add_item(item):
                    break
                packed += 1

    results = []
    for box in bins:
        result = {
            "boxno": box.boxno,
            "boxused": box.boxused,
            "itemsinbox": [
                f"{item.name} ({item.quantity}x)" if item.quantity > 1 else item.name for item in box.items
            ],
        }
        results.append(result)

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
