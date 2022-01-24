# https://gamedevelopment.tutsplus.com/tutorials/quick-tip-use-quadtrees-to-detect-likely-collisions-in-2d-space--gamedev-374
from random import randrange
import dearpygui.dearpygui as dpg

from Rectangle import Rectangle, DrawnRectangle
from Quadtree import Quadtree


def rand_coords(limit=500):
    """Paire de coordonnées aléatoires"""
    return (randrange(limit), randrange(limit))


def update():
    """Exécuté toutes les frames"""
    # On recrée l'arbre
    QUAD.clear()
    for objet in OBJETS:
        QUAD.insert(objet)

    # On parcourt tous les objets en trouvant quels objets chacun pourrait collide
    for objet in OBJETS:
        collisions_potentielles = set(QUAD.retrieve(objet))
        collisions_potentielles.discard(objet)
        # On peut maintenant vérifier les collisions seulement avec ces objets
        for autre in collisions_potentielles:
            objet.check_collision(autre)


def main():
    global OBJETS
    global QUAD

    DIMENSIONS_FENETRE = (400, 400)
    NB_OBJETS = 40

    OBJETS = []
    QUAD = Quadtree(level=0, bounds=Rectangle(0, 0, *[int(dim // 1.1) for dim in DIMENSIONS_FENETRE]))


    dpg.create_context()

    with dpg.window(tag="primary_window"):
        OBJETS = [
            DrawnRectangle(
                *rand_coords(int(DIMENSIONS_FENETRE[0] // 1.3)),
                30, 30,
                color=(0,0,0)
            ) for _ in range(NB_OBJETS)]

    dpg.set_primary_window("primary_window", True)

    with dpg.theme() as global_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (200, 200, 200))
    dpg.bind_theme(global_theme)


    dpg.create_viewport(width=DIMENSIONS_FENETRE[0], height=DIMENSIONS_FENETRE[1] + 20)
    dpg.setup_dearpygui()
    dpg.show_viewport()

    # below replaces, start_dearpygui()
    while dpg.is_dearpygui_running() and len(OBJETS) != 0:
        update()
        dpg.render_dearpygui_frame()
    dpg.destroy_context()

if __name__ == '__main__':
    main()