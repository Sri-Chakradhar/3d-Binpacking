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
            "stored": {
                "itemsinbox": box.itemsinbox,
                "itemquantity": {item.name: box.itemsinbox.count(item.name) for item in items}
            }, 
            "boxused": box.boxused
        }

        results.append(result)

    return jsonify(results)
