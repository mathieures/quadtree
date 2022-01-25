from Rectangle import Rectangle, DrawnRectangle
import color

class Quadtree:
    """A quad tree node"""
    MAX_OBJECTS = 5
    # MAX_OBJECTS = 10
    MAX_LEVELS = 5

    def __init__(self, window, level, bounds):
        self.window = window # the window where to draw the zones
        self.level = level # 0 being the root
        self.bounds = bounds # the 2D space the node is occupying (a Rectangle)
        self.objects = [] # the objects in these bounds (Rectangle objects)
        self.nodes = [None] * 4 # the children nodes

    def clear(self):
        """Clears the tree recursively"""
        self.objects.clear()
        for i, node in enumerate(self.nodes):
            if node is not None:
                node.clear() # Calls the child's clear() method
                self.nodes[i] = None

    def split(self):
        """Split the node in 4 new Quadtree objects"""
        sub_width = self.bounds.width // 2
        sub_height = self.bounds.height // 2
        x, y = self.bounds.x, self.bounds.y

        self.nodes[0] = Quadtree(self.window, self.level + 1, Rectangle(x, y, sub_width, sub_height)) # top left
        self.nodes[1] = Quadtree(self.window, self.level + 1, Rectangle(x + sub_width, y, sub_width, sub_height)) # top right
        self.nodes[2] = Quadtree(self.window, self.level + 1, Rectangle(x, y + sub_height, sub_width, sub_height)) # bottom left
        self.nodes[3] = Quadtree(self.window, self.level + 1, Rectangle(x + sub_width, y + sub_height, sub_width, sub_height)) # bottom right

        # Draw the zones for debugging purposes
        DrawnRectangle(x + sub_width, y, sub_width, sub_height, color=color.RED, parent=self.window)
        DrawnRectangle(x, y, sub_width, sub_height, color=color.RED, parent=self.window)
        DrawnRectangle(x, y + sub_height, sub_width, sub_height, color=color.RED, parent=self.window)
        DrawnRectangle(x + sub_width, y + sub_height, sub_width, sub_height, color=color.RED, parent=self.window)

    def get_index(self, rect):
        """
        Returns the index of the child node the object
        would belong to, or -1 if none correspond
        """
        index = -1

        vertical_midpoint = self.bounds.x + self.bounds.width // 2
        horizontal_midpoint = self.bounds.y + self.bounds.height // 2

        # Does the object fit in the top half?
        in_top_half = rect.y < horizontal_midpoint and rect.y + rect.height < horizontal_midpoint

        # Does the object fit in the bottom half?
        in_bottom_half = rect.y > horizontal_midpoint # Checking the origin is enough

        # If the object fits in the left half
        if rect.x < vertical_midpoint and rect.x + rect.width < vertical_midpoint:
            # If it fit in the top half then it's in the top left node
            if in_top_half:
                index = 0
            elif in_bottom_half:
                index = 2
        # Else if it fits in the right half
        elif rect.x > vertical_midpoint:
            if in_top_half:
                index = 1
            elif in_bottom_half:
                index = 3

        return index

    def insert(self, rect):
        """
        Inserts a Rectangle object in the quad tree.
        If the targeted node is full, it's split and
        its children are moved in the right nodes
        """
        # If the nodes has children, insert the object in one of them
        if self.nodes[0] is not None:
            index = self.get_index(rect)
            if index != -1:
                self.nodes[index].insert(rect)
                return

        # Either there is no child, or the object didn't fit in a child
        # Add the object to the node
        self.objects.append(rect)

        if len(self.objects) > self.MAX_OBJECTS and self.level < self.MAX_LEVELS:
            if self.nodes[0] is None:
                self.split()

            # Distribute the objects in the children nodes if they fit
            i = 0
            while i < len(self.objects):
                index = self.get_index(self.objects[i])
                if index != -1:
                    self.nodes[index].insert(self.objects.pop(i))
                else:
                    i += 1

    def retrieve(self, rect, potential_collisions=None):
        """
        Returns all the objects that could
        collide with the given object
        """
        if potential_collisions is None:
            potential_collisions = []

        index = self.get_index(rect)
        if index != -1 and self.nodes[0] is not None:
            self.nodes[index].retrieve(rect, potential_collisions)

        potential_collisions.extend(self.objects)
        # print(f"{potential_collisions}")
        return potential_collisions