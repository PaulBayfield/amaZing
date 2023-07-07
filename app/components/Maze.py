from random import randint, shuffle, choice


class Maze:
    """
    Classe Labyrinthe
    Représentation sous forme de graphe non-orienté
    dont chaque sommet est une cellule (un tuple (l,c))
    et dont la structure est représentée par un dictionnaire
      - clés : sommets
      - valeurs : ensemble des sommets voisins accessibles
    """
    def __init__(self, height, width, empty: bool) -> None:
        """
        Constructeur d'un labyrinthe de height cellules de haut
        et de width cellules de large
        Les voisinages sont initialisés à des ensembles vides
        Remarque : dans le labyrinthe créé, chaque cellule est complètement emmurée
        Lorsque empty est initalisés à True, les murs disparaissent.
        """
        self.height    = height
        self.width     = width
        self.neighbors = {(i,j): set() for i in range(height) for j in range (width)}
        if empty:
            # Parcours les cellules
            for n in self.neighbors:
                data = []
                # Conditions pour savoir si la cellule est : dans un coins, collés aux extrémités, au milieu.
                if n[0]-1 >= 0:
                    data.append((n[0]-1, n[1]))
                if n[1]-1 >= 0:
                    data.append((n[0], n[1]-1))
                if n[0]+1 < self.height:
                    data.append((n[0]+1, n[1]))
                if n[1]+1 < self.width:
                    data.append((n[0], n[1]+1))
                # Retrait des murs
                self.neighbors[n] = set(data)

        self.items = []
        for _ in range(self.height):
            temp = []
            for _ in range(self.width):
                temp.append(0)
                
            self.items.append(temp)
                        
    
    def __str__(self):
        """
        Représentation textuelle d'un objet Maze (en utilisant des caractères ascii)
        
        :return: chaîne (str) : chaîne de caractères représentant le labyrinthe
        """
        txt = ""
        # Première ligne
        txt += "┏"
        for j in range(self.width-1):
            txt += "━━━┳"
        txt += "━━━┓\n"
        txt += "┃"
        for j in range(self.width-1):
            txt += "   ┃" if (0,j+1) not in self.neighbors[(0,j)] else "    "
        txt += "   ┃\n"
        # Lignes normales
        for i in range(self.height-1):
            txt += "┣"
            for j in range(self.width-1):
                txt += "━━━╋" if (i+1,j) not in self.neighbors[(i,j)] else "   ╋"
            txt += "━━━┫\n" if (i+1,self.width-1) not in self.neighbors[(i,self.width-1)] else "   ┫\n"
            txt += "┃"
            for j in range(self.width):
                txt += "   ┃" if (i+1,j+1) not in self.neighbors[(i+1,j)] else "    "
            txt += "\n"
        # Bas du tableau
        txt += "┗"
        for i in range(self.width-1):
            txt += "━━━┻"
        txt += "━━━┛\n"

        return txt
        
    
    def add_wall(self, c1: tuple, c2: tuple) -> None:
        """
        Ajoute d'un mur entre les cellules c1 et c2
        
        :param: c1 (tuple): Cellule 1
        :param: c2 (tuple): Cellule 2
        """
        # Facultatif : on teste si les sommets sont bien dans le labyrinthe
        assert 0 <= c1[0] < self.height and \
            0 <= c1[1] < self.width and \
            0 <= c2[0] < self.height and \
            0 <= c2[1] < self.width, \
            f"Erreur lors de l'ajout d'un mur entre {c1} et {c2} : les coordonnées de sont pas compatibles avec les dimensions du labyrinthe"

        # Ajout du mur
        if c2 in self.neighbors[c1]:      # Si c2 est dans les voisines de c1
            self.neighbors[c1].remove(c2) # on le retire
        if c1 in self.neighbors[c2]:      # Si c3 est dans les voisines de c2
            self.neighbors[c2].remove(c1) # on le retire
    
    
    def remove_wall(self, c1: tuple, c2: tuple) -> None:
        """
        Retire le mur entre les deux cellules c1 et c2.
        
        
        :param: c1 (tuple): Cellule 1
        :param: c2 (tuple): Cellule 2
        """
        assert 0 <= c1[0] < self.height and \
            0 <= c1[1] < self.width and \
            0 <= c2[0] < self.height and \
            0 <= c2[1] < self.width, \
            f"Erreur lors de la suppression d'un mur entre {c1} et {c2} : les coordonnées de sont pas compatibles avec les dimensions du labyrinthe"
        assert c1[0] == c2[0] and \
            (c1[1] == c2[1] -1 or \
            c2[1] == c1[1]-1) or \
            c1[1] == c2[1] and \
            (c1[0] == c2[0]-1 or \
             c2[0] == c1[0]-1), \
             f"Erreur lors de la suppression d'un mur entre {c1} et {c2} : les coordonnées ne sont pas bien alignées dans le labyrinthe"
             
        liste = list(self.neighbors[c1])
        liste.append(c2)
        self.neighbors[c1] = set(liste)
        
        liste = list(self.neighbors[c2])
        liste.append(c1)
        self.neighbors[c2] = set(liste)

        
    def get_walls(self) -> list:
        """
        Retourne la liste de tous les murs sous la forme d’une liste de tuple de cellules
        
        :return: data (list): liste de coordonées
        """
        data = []
        for n in self.neighbors:
            neighbors = []
            if n[0]-1 >= 0:
                neighbors.append((n[0]-1, n[1]))
            if n[1]-1 >= 0:
                neighbors.append((n[0], n[1]-1))
            if n[0]+1 < self.height:
                neighbors.append((n[0]+1, n[1]))
            if n[1]+1 < self.width:
                neighbors.append((n[0], n[1]+1))
            
            for m in neighbors:
                if m not in list(self.neighbors[n]) and [m, n] not in data:
                    data.append([n, m])

        return data
    
    
    def fill(self) -> None:
        """
        Ajoute tous les murs possibles dans le labyrinthe
        """
        for n in self.neighbors:
            self.neighbors[n] = {}

            
    def empty(self) -> None:
        """
        Supprime tous les murs du labyrinthe
        """
        for n in self.neighbors:
            data = []
            if n[0]-1 >= 0:
                data.append((n[0]-1, n[1]))
            if n[1]-1 >= 0:
                data.append((n[0], n[1]-1))
            if n[0]+1 < self.height:
                data.append((n[0]+1, n[1]))
            if n[1]+1 < self.width:
                data.append((n[0], n[1]+1))

            self.neighbors[n] = set(data)
            
   
    def get_contiguous_cells(self, cell: tuple) -> list:
        """
        Retourne la liste des cellules contigües à c dans la grille (sans s’occuper des éventuels murs)
        
        :param: cell (tuple): Une cellule
        :return: data (list): 
        """
        assert 0 <= cell[0] < self.height and \
            0 <= cell[1] < self.width, \
            f"Erreur - {cell}: les coordonnées de sont pas compatibles avec les dimensions du labyrinthe"
        
        data = []
        if cell[0]-1 >= 0:
            data.append((cell[0]-1, cell[1]))
        if cell[1]-1 >= 0:
            data.append((cell[0], cell[1]-1))
        if cell[0]+1 < self.height:
            data.append((cell[0]+1, cell[1]))
        if cell[1]+1 < self.width:
            data.append((cell[0], cell[1]+1))
            
        return data

    
    def get_reachable_cells(self, cell: tuple) -> list:
        """
        Retourne la liste des cellules accessibles depuis c dans la grille
        
        :param: cell (tuple): Une cellule
        :return: data (list): 
        """
        assert 0 <= cell[0] < self.height and \
            0 <= cell[1] < self.width, \
            f"Erreur - {cell}: les coordonnées de sont pas compatibles avec les dimensions du labyrinthe"
        
        data = []
        if cell[0]-1 >= 0 and (cell[0]-1, cell[1]) in self.neighbors[cell]:
               data.append((cell[0]-1, cell[1]))
        if cell[1]-1 >= 0 and (cell[0], cell[1]-1) in self.neighbors[cell]:
               data.append((cell[0], cell[1]-1))
        if cell[0]+1 < self.height and (cell[0]+1, cell[1]) in self.neighbors[cell]:
               data.append((cell[0]+1, cell[1]))
        if cell[1]+1 < self.width and (cell[0], cell[1]+1) in self.neighbors[cell]:
               data.append((cell[0], cell[1]+1))      
                
        return data
   

    @classmethod
    def gen_btree(cls, h: int, w: int):
        """
        Méthode de classe qui génère une labyrinthe à h lignes et w colonnes, en utilisant l’algorithme de construction par arbre binaire.
        
        :param: h (int): La hauteur du Labyrinthe
        :param: w (int): La largeur du Labyrinthe
        :return: laby (Maze): Labyrinthe
        """
        laby = cls(h, w, empty=False)
        
        for cell in laby.neighbors:
            data = []
            if cell[0]+1 < laby.height:
                data.append((cell[0]+1, cell[1]))
            if cell[1]+1 < laby.width:
                data.append((cell[0], cell[1]+1))
        
            if len(data) == 1:
                laby.remove_wall(cell, data[0])
            elif len(data) == 2:
                laby.remove_wall(cell, data[randint(0,1)])
            
        return laby
    
    
    @classmethod
    def gen_sidewinder(cls, h: int, w: int):
        """
        Méthode de classe qui génère un labyrinthe à h lignes et w colonnes, en utilisant l’algorithme de construction par arbre binaire.
        
        :param: h (int): La hauteur du labyrinthe
        :param: w (int): La largeur du labyrinthe
        :return: laby (Maze): Labyrinthe
        """
        laby = cls(h, w, empty=False)
        
        for i in range(h-1):
            sequence = []
            
            for j in range(w-1):
                sequence.append((i,j))
                pileOuFace = randint(0,1)
                
                if pileOuFace == 0:
                    laby.remove_wall((i, j), (i, j+1))
                    
                else:
                    cellule = sequence[randint(0, len(sequence))-1]
                    celluleSud = (cellule[0]+1, cellule[1])
                    laby.remove_wall(cellule, celluleSud)
                    sequence = []
            sequence.append((i, w-1))
            
            cellule = sequence[randint(0, len(sequence))-1]
            celluleSud = (cellule[0]+1, cellule[1])
            laby.remove_wall(cellule, celluleSud)
                
        for i in range(w-1):
            cellule = (h-1, i)
            celluleEst = (cellule[0], cellule[1]+1)
            laby.remove_wall(cellule, celluleEst)
            
        return laby
    

    @classmethod
    def gen_exploration(cls, h,w):
        """
        Méthode de classe qui génère un labyrinthe, à h lignes et w colonnes, parfait, avec l’algorithme d’exploration exhaustive.

        :param: h (int): La hauteur du labyrinthe
        :param: w (int): La largeur du labyrinthe
        :return: laby (Maze): Labyrinthe
        """
        laby = cls(h, w, empty=False)
        cellRand = (randint(0,h-1), randint(0,w-1))
        
        markCell = [cellRand]
        Pile = [cellRand]

        while len(Pile) > 0:
            cellule = Pile.pop()
            voisinPasVisiter = []

            for cell in laby.get_contiguous_cells(cellule):
                if cell not in markCell:
                    voisinPasVisiter.append(cell)
                
            if voisinPasVisiter:
                Pile.append(cellule)
                    
                voisineAlea = voisinPasVisiter[randint(0,len(voisinPasVisiter)-1)]
                
                laby.remove_wall(cellule, voisineAlea)
                     
                markCell.append(voisineAlea)
                Pile.append(voisineAlea)
            
        return laby

    
    @classmethod
    def gen_fusion(cls, h: int, w: int):
        """
        Méthode de classe qui génère un labyrinthe, à h lignes et w colonnes, parfait, avec l’algorithme de fusion de chemin.
        
        :param: h (int): La hauteur du labyrinthe
        :param: w (int): La largeur du labyrinthe
        :return: laby (Maze): Labyrinthe
        """

        # On remplit le labyrinthe avec tous les murs possibles
        laby = cls(h, w, empty=False)
        
        
        # On labélise les cellules de 1 à n
        data = []
        count = 1
        for i in range(0, h):
            row = []
            for j in range(0, w):
                row.append(count)
                count += 1
                
            data.append(row)
            
        
        # On extrait la liste de tous les murs et on les « mélange » (on les permute aléatoirement)
        cellules = laby.get_walls()
        shuffle(cellules)
        
        # Pour chaque mur de la liste :
        for mur in cellules:
            c1 = data[mur[0][0]][mur[0][1]]
            c2 = data[mur[1][0]][mur[1][1]]
            if c1 != c2:
                # On casse le mur
                laby.remove_wall(mur[0], mur[1])
                
                # On affecte le label de l’une des deux cellules, à l’autre, et à toutes celles qui ont le même label que la deuxième
                data[mur[0][0]][mur[0][1]] = c2
                
                for i in range(0, h):
                    for j in range(0, w):
                        if data[i][j] == c1:
                            data[i][j] = c2
            
        return laby

    
    @classmethod
    def gen_wilson(cls, h: int, w: int):
        """
        Méthode de classe qui génère un labyrinthe, à h lignes et w colonnes, parfait, avec l’algorithme de Wilson.
        
        :param: h (int): La hauteur du labyrinthe
        :param: w (int): La largeur du labyrinthe
        :return: laby (Maze): Labyrinthe
        """        
        laby = cls(h, w, empty=False)
        cellules = []
        for i in range(h):
            for j in range(w):
                cellules.append((i, j))
        
        # Choisir une cellule au hasard sur la grille et la marquer
        cellHasard = (randint(0, h-1), randint(0, w-1))
        cellMarque = [cellHasard]
        
        # Tant qu’il reste des cellules non marquées :
        while len(cellules) != len(cellMarque):
            
            # Choisir une cellule de départ au hasard, parmi les cellules non marquées
            depart = (randint(0, h-1), randint(0, w-1))
            while depart in cellMarque:
                depart = (randint(0, h-1), randint(0, w-1))

            
            # Effectuer une marche aléatoire jusqu’à ce qu’une cellule marquée soit atteinte (en cas de boucle, si la tête du snake se
            # mord la queue, « couper » la boucle formée [autrement dit, supprimer toutes étapes depuis le précédent passage])
            chemin = [depart]
            while chemin[-1] not in cellMarque:
                cellRand = choice(laby.get_contiguous_cells(chemin[-1])) 
                if cellRand in chemin:
                    idx = chemin.index(cellRand)
                    chemin = chemin[:idx+1]
                else:
                    chemin.append(cellRand)
         
            # Marquer chaque cellule du chemin, et casser tous les murs rencontrés, jusqu’à la cellule marquée
            for i in range(len(chemin)-1):
                laby.remove_wall(chemin[i], chemin[i+1])
            
            cellMarque.extend(chemin[:-1])

        return laby
    
    
    def overlay(self, content: dict = None) -> str:
        """
        Rendu en mode texte, sur la sortie standard, d'un labyrinthe avec du contenu dans les cellules
        
        :param: content (dict) : dictionnaire tq content[cell] contient le caractère à afficher au milieu de la cellule
        :return: txt (string)
        """
        if content is None:
            content = {(i,j):' ' for i in range(self.height) for j in range(self.width)}
        else:
            c = {(i, j): ' ' for i in range(self.height) for j in range(self.width) if (i,j) not in content}
            content = {**content, **c}
            #content = content | {(i, j): ' ' for i in range(self.height) for j in range(self.width) if (i,j) not in content}
            
        txt = r""
        # Première ligne
        txt += "┏"
        for j in range(self.width-1):
            txt += "━━━┳"
        txt += "━━━┓\n"
        txt += "┃"
        for j in range(self.width-1):
            txt += " "+content[(0,j)]+" ┃" if (0,j+1) not in self.neighbors[(0,j)] else " "+content[(0,j)]+"  "
        txt += " "+content[(0,self.width-1)]+" ┃\n"
        # Lignes normales
        for i in range(self.height-1):
            txt += "┣"
            for j in range(self.width-1):
                txt += "━━━╋" if (i+1,j) not in self.neighbors[(i,j)] else "   ╋"
            txt += "━━━┫\n" if (i+1,self.width-1) not in self.neighbors[(i,self.width-1)] else "   ┫\n"
            txt += "┃"
            for j in range(self.width):
                txt += " "+content[(i+1,j)]+" ┃" if (i+1,j+1) not in self.neighbors[(i+1,j)] else " "+content[(i+1,j)]+"  "
            txt += "\n"
        # Bas du tableau
        txt += "┗"
        for i in range(self.width-1):
            txt += "━━━┻"
        txt += "━━━┛\n"
        return txt 
    
    
    def solve_dfs(self, D: tuple, A: tuple) -> list:
        """ 
        Parcous en profondeur du Labyrinthe.
        
        :param: D (tuple): La celle de Départ
        :param: A (tuple): La cellule d'Arrivée
        :return: chemin (list): Le chemin
        """
        
        # Placer D dans la struture d’attente (file ou pile) et marquer D
        Pile = [D]
        cellMarque = [D]
        
        # Mémoriser l’élément prédécesseur de D comme étant D
        predecesseurs = {D: D}
        
        cellules = self.get_walls()
        run = True
        
        # Tant qu’il reste des cellules non-marquées :
        while run:
            c = Pile.pop()
            if c == A:
                run = False
            else:
                for cell in self.get_reachable_cells(c):
                    if cell not in cellMarque:
                        cellMarque.append(cell)
                        Pile.append(cell)
                        predecesseurs[cell] = c
                
        # Initialiser c à A
        chemin = []
        c = A
        
        # Tant que c n’est pas D :
        while c != D:
            
            # ajouter c au chemin
            chemin.append(c)
            
            # mettre le prédécesseur de c dans c
            c = predecesseurs[c]
        
        # Ajouter D au chemin
        chemin.append(D)
        
        return chemin
    
    
    def solve_bfs(self, D: tuple, A: tuple) -> list:
        """ 
        Parcous en largeur du Labyrinthe.
        
        :param: D (tuple): La celle de Départ
        :param: A (tuple): La cellule d'Arrivée
        :return: chemin (list): Le chemin
        """
        
        # Placer D dans la struture d’attente (file ou pile) et marquer D
        File = [D]
        cellMarque = [D]
        
        # Mémoriser l’élément prédécesseur de D comme étant D
        predecesseurs = {D: D}
        
        cellules = self.get_walls()
        run = True
        
        # Tant qu’il reste des cellules non-marquées :
        while run:
            c = File.pop(0)
            if c == A:
                run = False
            else:
                for cell in self.get_reachable_cells(c):
                    if cell not in cellMarque:
                        cellMarque.append(cell)
                        File.append(cell)
                        predecesseurs[cell] = c
                
        # Initialiser c à A
        chemin = []
        c = A

        # Tant que c n’est pas D :
        while c != D:
            
            # ajouter c au chemin
            chemin.append(c)
            
            # mettre le prédécesseur de c dans c
            c = predecesseurs[c]
        
        # Ajouter D au chemin
        chemin.append(D)
        
        return chemin


    def distance_geo(self, c1: tuple, c2: tuple) -> int:
        """ 
        Retourne le nombre minimal de déplacements nécessaires sur le graphe pour aller de c1 à c2.
        
        :param: c1 (tuple): La celle de Départ
        :param: c2 (tuple): La cellule d'Arrivée
        :return: distance (int)
        """
        return len(self.solve_dfs(c1, c2))
        
        
    def distance_man(self, c1: tuple, c2: tuple) -> int:
        """ 
        Retourne le nombre minimal de déplacements nécessaires pour aller de c2 à c1 si le labyrinthe était vide de tout mur.
        
        :param: c1 (tuple): La celle de Départ
        :param: c2 (tuple): La cellule d'Arrivée
        :return: distance (int)
        """
        return abs(c1[0] - c2[0]) + abs(c1[1] - c2[1])
    
    
    def solve_rhr(self, start: tuple, stop: tuple) -> list:
        """ 
        Parcous en utlisant l'algorithme de la "main droite".
        
        :param: start (tuple): La celle de Départ
        :param: stop (tuple): La cellule d'Arrivée
        :return: chemin (list): Le chemin
        """
        cell = start
        chemin = [start]
        direction = "S"
        
        ordres = {
            "S": ["O", "S", "E", "N"],
            "O": ["N", "O", "S", "E"],
            "N": ["E", "N", "O", "S"],
            "E": ["S", "E", "N", "O"]
        }
        
        while cell != stop:
            cellule = None
            
            for ordre in ordres[direction]:
                if ordre == "O":
                    # Ouest
                    if cell[1]-1 >= 0 and (cell[0], cell[1]-1) in self.neighbors[cell] and \
                    cell[1]-1 >= 0 and (cell[0], cell[1]-1) and not cellule:
                        cellule = (cell[0], cell[1]-1)
                        direction = "O"
                elif ordre == "S":
                    # Sud
                    if cell[0]+1 < self.height and (cell[0]+1, cell[1]) in self.neighbors[cell] and \
                    cell[0]+1 < self.height and (cell[0]+1, cell[1]) and not cellule:
                        cellule = (cell[0]+1, cell[1])
                        direction = "S"
                elif ordre == "E":    
                    # Est
                    if cell[1]+1 < self.width and (cell[0], cell[1]+1) in self.neighbors[cell] and \
                    cell[1]+1 < self.width and (cell[0], cell[1]+1) and not cellule:
                        cellule = (cell[0], cell[1]+1)
                        direction = "E"
                elif ordre == "N":
                    # Nord 
                    if cell[0]-1 >= 0 and (cell[0]-1, cell[1]) in self.neighbors[cell] and \
                    cell[0]-1 >= 0 and (cell[0]-1, cell[1]) and not cellule:
                        cellule = (cell[0]-1, cell[1])
                        direction = "N"

            # Ajout ou suppression de la cellule dans le chemin
            if cellule in chemin:
                chemin.remove(cellule)
            else:
                chemin.append(cell)

            # Préparation de la prochaine itération...
            cell = cellule

        chemin.append(stop)

        return chemin
    
        
    def solve_rhro(self, start: tuple, stop: tuple) -> tuple:
        """ 
        Parcous en utlisant l'algorithme de la "main droite" qui renvoie toutes les cellules parcourues.
        
        Note : solve_rhr Overlay - Cette fonction n'est pas dans l'énoncé mais elle permet d'y voir un peu plus clair dans
               l'éxecution de cette fonction. Elle renvoie le chemin et toutes les cellules parcourues. 
               Il suffit ensuite de concatener les eux dictionnaires puis d'afficher "l'overlay".
        
        :param: start (tuple): La celle de Départ
        :param: stop (tuple): La cellule d'Arrivée
        :return: (chemin, cellules) (tuple): Le chemin et les cellules parcourues
        """
        cell = start
        chemin = [start]
        cellules = []
        direction = "S"
        
        ordres = {
            "S": ["O", "S", "E", "N"],
            "O": ["N", "O", "S", "E"],
            "N": ["E", "N", "O", "S"],
            "E": ["S", "E", "N", "O"]
        }
        
        while cell != stop:
            cellule = None
            
            for ordre in ordres[direction]:
                if ordre == "O":
                    # Ouest
                    if cell[1]-1 >= 0 and (cell[0], cell[1]-1) in self.neighbors[cell] and \
                    cell[1]-1 >= 0 and (cell[0], cell[1]-1) and not cellule:
                        cellule = (cell[0], cell[1]-1)
                        direction = "O"
                elif ordre == "S":
                    # Sud
                    if cell[0]+1 < self.height and (cell[0]+1, cell[1]) in self.neighbors[cell] and \
                    cell[0]+1 < self.height and (cell[0]+1, cell[1]) and not cellule:
                        cellule = (cell[0]+1, cell[1])
                        direction = "S"
                elif ordre == "E":    
                    # Est
                    if cell[1]+1 < self.width and (cell[0], cell[1]+1) in self.neighbors[cell] and \
                    cell[1]+1 < self.width and (cell[0], cell[1]+1) and not cellule:
                        cellule = (cell[0], cell[1]+1)
                        direction = "E"
                elif ordre == "N":
                    # Nord 
                    if cell[0]-1 >= 0 and (cell[0]-1, cell[1]) in self.neighbors[cell] and \
                    cell[0]-1 >= 0 and (cell[0]-1, cell[1]) and not cellule:
                        cellule = (cell[0]-1, cell[1])
                        direction = "N"
            
            # Ajout ou suppression de la cellule dans le chemin
            if cellule in chemin:
                chemin.remove(cellule)
            else:
                chemin.append(cell)
            
            cellules.append(cellule)

            # Préparation de la prochaine itération...
            cell = cellule

        chemin.append(stop)

        return (chemin, cellules)       


    def isValid(self, x, y):
        return self.items[x][y] == 0

    
    def setItem(self, x, y, priority):
        self.items[x][y] = priority


    def getItem(self, x, y):
        return self.items[x][y]


    def reachable(self, x, y, x1, y1):
        return (y, x) in self.get_reachable_cells((y1, x1))
