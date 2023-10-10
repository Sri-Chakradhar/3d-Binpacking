typeofitems = int(input())
typeofbins = int(input())

class Box:
    def __init__(self, boxno, width, height, depth, capacity, available):
        self.boxno = boxno
        self.width = width
        self.height = height
        self.depth = depth
        self.capacity = capacity
        self.remaining_volume = width * height * depth
        self.items = []
        self.boxused = 0
        self.itemsinbox = []
        self.available = available

    def add_item(self, item):
        if self.remaining_volume >= item.volume and not item.occupied:
            if self.boxused < self.available:  # Check available space
                self.items.append(item)
                self.remaining_volume -= item.volume
                return True
        return False

class Item:
    def __init__(self, name, width, height, depth, weight, orientation=None):
        self.name = name
        self.width = width
        self.height = height
        self.depth = depth
        self.weight = weight
        self.orientation = orientation
        self.volume = width * height * depth
        self.occupied = False

items = []  # Create a list to store items
for i in range(typeofitems):
    itemname = input()
    itemwidth = int(input())
    itemheight = int(input())
    itemdepth = int(input())
    itemweight = int(input())
    item = Item(itemname, itemwidth, itemheight, itemdepth, itemweight)
    items.append(item)

bins = []  # Create a list to store bins
for i in range(typeofbins):
    boxno = int(input())
    boxwidth = int(input())
    boxheight = int(input())
    boxdepth = int(input())
    boxcapacity = int(input())
    available = int(input())
    box = Box(boxno, boxwidth, boxheight, boxdepth, boxcapacity, available)
    bins.append(box)

for item in items:
    for box in bins:
        if box.remaining_volume >= item.volume and not item.occupied:
            if box.add_item(item):
                item.occupied = True
                box.itemsinbox.append(item.name)
                box.boxused += 1

for box in bins:
    print(f"Box {box.boxno}:")
    for itemname in box.itemsinbox:
        print(f"  {itemname}")
    print(f"Box used: {box.boxused}")
