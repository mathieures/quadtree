# https://gamedevelopment.tutsplus.com/tutorials/quick-tip-use-quadtrees-to-detect-likely-collisions-in-2d-space--gamedev-374
from random import randrange
import dearpygui.dearpygui as dpg

from Rectangle import Rectangle, DrawnRectangle
from Quadtree import Quadtree

import color


def rand_coords(limit=500):
    """Paire de coordonnées aléatoires"""
    return (randrange(limit), randrange(limit))


def update():
    """
    Executed every frame (we don't need it in this project
    since the objects don't move, but it's an example)
    """
    # Recreate the tree
    QUAD.clear()
    for obj in OBJECTS:
        QUAD.insert(obj)

    # Loop through the objects to find which objects each could collide with
    for obj in OBJECTS:
        potential_collisions = set(QUAD.retrieve(obj))
        potential_collisions.discard(obj)
        # We can now check collisions only with these objects
        for other in potential_collisions:
            obj.check_collision(other)


## Main ##

DIMENSIONS = (400, 400)
OBJECT_COUNT = 40
WINDOW = "primary_window"

OBJECTS = []
QUAD = Quadtree(WINDOW, level=0, bounds=Rectangle(0, 0, *[int(dim // 1.1) for dim in DIMENSIONS]))


dpg.create_context()

with dpg.window(tag=WINDOW):
    OBJECTS = [
        DrawnRectangle(
            *rand_coords(int(DIMENSIONS[0] // 1.3)),
            30, 30,
            color=color.BLACK
        ) for _ in range(OBJECT_COUNT)]

dpg.set_primary_window(WINDOW, True)

with dpg.theme() as global_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (200, 200, 200))
dpg.bind_theme(global_theme)


dpg.create_viewport(width=DIMENSIONS[0], height=DIMENSIONS[1] + 20)
dpg.setup_dearpygui()
dpg.show_viewport()

# Main loop
while dpg.is_dearpygui_running() and len(OBJECTS) != 0:
    update()
    dpg.render_dearpygui_frame()
dpg.destroy_context()