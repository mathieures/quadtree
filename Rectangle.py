import dearpygui.dearpygui as dpg
import color


class Rectangle:
    """A rectangle, a point with dimensions"""
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def __repr__(self):
        return f"{type(self).__name__}, {self.x, self.y, self.width, self.height}"


class DrawnRectangle(Rectangle):
    """A rectangle, but graphically displayed"""
    def __init__(self, x, y, width, height, **kwargs):
        super().__init__(x, y, width, height)

        self.tag = dpg.draw_rectangle(
            (self.x, self.y),
            (self.x + self.width, self.y + self.height),
            **kwargs
        )

    def check_collision(self, objet):
        """Check collisions with the given object"""
        self_x2, self_y2 = self.x + self.width, self.y + self.height
        objet_x2, objet_y2 = objet.x + objet.width, objet.y + objet.height

        if (self.x < objet_x2 and self_x2 > objet.x) and (
            self.y < objet_y2 and self_y2 > objet.y):
                self.action_collision()
                objet.action_collision()

    def action_collision(self):
        """Callback function used after a collision"""
        dpg.configure_item(self.tag, fill=color.GREEN)