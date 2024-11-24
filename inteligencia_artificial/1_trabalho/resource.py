from configs import RESOURCE_TYPES

class Resource:
    def __init__(self, resource_type, x, y):
        if resource_type not in RESOURCE_TYPES:
            raise ValueError(f"Resource type '{resource_type}' not found.")
        
        self.type = resource_type
        self.x = x
        self.y = y
        self.color = RESOURCE_TYPES[resource_type]["color"]
        self.size = RESOURCE_TYPES[resource_type]["size"]
        self.utility = RESOURCE_TYPES[resource_type]["utility"]
        self.agents_required = RESOURCE_TYPES[resource_type]["agents_required"]
        self.img = RESOURCE_TYPES[resource_type]["img"]
        self.collected = False

    def __repr__(self):
        return f"Resource(type={self.type}, x={self.x}, y={self.y}, size={self.size}, utility={self.utility})"
