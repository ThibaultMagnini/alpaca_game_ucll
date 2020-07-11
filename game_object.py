

class Object:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def world_to_viewplane_coordinates(self, px, py, pz):
        t = -pz / (self.z + -pz)
        x = self.x * t
        y = py + ((self.y - py) * t)
        return x, y, 0

    def viewplane_to_world_coordinates(self, px, py, pz):
        t = py / (py - self.y)
        x = self.x * t
        z = t - 1 * -pz
        return x, 0, z

    def screen_to_viewplane_coordinates(self, px, py, WIDTH, HEIGHT):
        x = (px - WIDTH / 2) / WIDTH
        y = 1 - py / HEIGHT
        return x, y

    def viewplane_to_screen_coordinates(self, px, py, WIDTH, HEIGHT):
        x = px * WIDTH + (WIDTH / 2)
        y = (1 - py) * HEIGHT
        return x, y
