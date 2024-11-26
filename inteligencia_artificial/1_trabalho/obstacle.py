from configs import OBSTACLE_TYPES

class Obstacle:
    def __init__(self, obstacle_type, x, y):
        self.type = obstacle_type
        self.x = x
        self.y = y
        self.color = OBSTACLE_TYPES[obstacle_type]["color"]
        self.img = OBSTACLE_TYPES[obstacle_type]["img"]

    def __repr__(self):
        return f"Obstacle(type={self.type}, x={self.x}, y={self.y})"
