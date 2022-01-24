from Rectangle import Rectangle, DrawnRectangle


class Quadtree:
    """Un quadtree, ou arbre quartique"""
    MAX_OBJECTS = 5
    # MAX_OBJECTS = 10
    MAX_LEVELS = 5

    def __init__(self, level, bounds):
        self.level = level # 0 étant la racine
        self.bounds = bounds # l'espace 2D que le node occupe, un Rectangle
        self.objects = [] # liste d'objets, ici pour l'exemple des objets Rectangle
        self.nodes = [None] * 4 # les 4 noeuds fils

    def clear(self):
        """Efface récursivement le Quadtree"""
        self.objects.clear()
        for i, node in enumerate(self.nodes):
            if node is not None:
                node.clear() # appelle la méthode clear() du Quadtree fils
                self.nodes[i] = None

    def split(self):
        """Sépare le Quadtree en 4 noeuds Quadtree fils"""
        sub_width = self.bounds.width // 2
        sub_height = self.bounds.height // 2
        x, y = self.bounds.x, self.bounds.y

        self.nodes[0] = Quadtree(self.level + 1, Rectangle(x + sub_width, y, sub_width, sub_height)) # en haut à droite
        self.nodes[1] = Quadtree(self.level + 1, Rectangle(x, y, sub_width, sub_height)) # en haut à gauche
        self.nodes[2] = Quadtree(self.level + 1, Rectangle(x, y + sub_height, sub_width, sub_height)) # en bas à gauche
        self.nodes[3] = Quadtree(self.level + 1, Rectangle(x + sub_width, y + sub_height, sub_width, sub_height)) # en bas à droite

        # On dessine les zones, pour le debug
        DrawnRectangle(x + sub_width, y, sub_width, sub_height, color=(255, 0, 0), parent="primary_window")
        DrawnRectangle(x, y, sub_width, sub_height, color=(255, 0, 0), parent="primary_window")
        DrawnRectangle(x, y + sub_height, sub_width, sub_height, color=(255, 0, 0), parent="primary_window")
        DrawnRectangle(x + sub_width, y + sub_height, sub_width, sub_height, color=(255, 0, 0), parent="primary_window")

    def get_index(self, rect):
        """
        Retourne l'indice du fils dans lequel l'objet passé
        en paramètre devra aller, ou -1 s'il n'est dans aucun
        """
        index = -1

        vertical_midpoint = self.bounds.x + self.bounds.width // 2
        horizontal_midpoint = self.bounds.y + self.bounds.height // 2

        # Est-ce que l'objet peut complètement tenir dans la moitié haute ?
        in_top_half = rect.y < horizontal_midpoint and rect.y + rect.height < horizontal_midpoint

        # Est-ce que l'objet peut complètement tenir dans la moitié basse ?
        in_bottom_half = rect.y > horizontal_midpoint # on ne teste que l'origine car ce n'est que ça qui importe

        # S'il peut complètement tenir dans la partie gauche
        if rect.x < vertical_midpoint and rect.x + rect.width < vertical_midpoint:
            # S'il tenait dans la partie haute, il est en haut à gauche
            if in_top_half:
                index = 1
            elif in_bottom_half:
                index = 2
        # S'il peut complètement tenir dans la partie droite
        elif rect.x > vertical_midpoint:
            if in_top_half:
                index = 0
            elif in_bottom_half:
                index = 3

        return index

    def insert(self, rect):
        """
        Insère un objet Rectangle dans le Quadtree.
        Si le noeud cible est rempli, il est séparé
        et on met ses noeuds fils dans les bons noeuds
        """
        # Si le node a des enfants, on l'insère dans un enfant
        if self.nodes[0] is not None:
            index = self.get_index(rect)
            if index != -1:
                self.nodes[index].insert(rect)
                return

        # Sinon soit l'objet ne rentre pas soit il n'y a pas d'enfant
        # On ajoute l'objet au node
        self.objects.append(rect)

        if len(self.objects) > self.MAX_OBJECTS and self.level < self.MAX_LEVELS:
            if self.nodes[0] is None:
                self.split()

            # On répartit les objets dans les enfants
            i = 0
            while i < len(self.objects):
                index = self.get_index(self.objects[i])
                if index != -1:
                    self.nodes[index].insert(self.objects.pop(i))
                else:
                    i += 1

    def retrieve(self, rect, collisions_potentielles=None):
        """
        Retourne tous les objets qui pourraient
        collide avec l'objet donné en paramètre
        """
        if collisions_potentielles is None:
            collisions_potentielles = []

        index = self.get_index(rect)
        if index != -1 and self.nodes[0] is not None:
            self.nodes[index].retrieve(rect, collisions_potentielles)

        collisions_potentielles.extend(self.objects)
        # print(f"{collisions_potentielles}")
        return collisions_potentielles