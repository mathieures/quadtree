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
    Exécuté toutes les frames
    Dans ce projet on n'en a pas besoin en réalité, car
    les objets ne bougent pas, mais c'est pour l'exemple
    """
    # On recrée l'arbre
    QUAD.clear()
    for obj in OBJECTS:
        QUAD.insert(obj)

    # On parcourt tous les objets en trouvant avec quels objeCts chacun pourrait collide
    for obj in OBJECTS:
        potential_collisions = set(QUAD.retrieve(obj))
        potential_collisions.discard(obj)
        # On peut maintenant vérifier les collisions seulement avec ces objeCts
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

# below replaces `start_dearpygui()`
while dpg.is_dearpygui_running() and len(OBJECTS) != 0:
    update()
    dpg.render_dearpygui_frame()
dpg.destroy_context()