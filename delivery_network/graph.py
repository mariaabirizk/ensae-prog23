class Graph:
    """
    A class representing graphs as adjacency lists and implementing various algorithms on the graphs. Graphs in the class are not oriented. 
    Attributes: 
    -----------
    nodes: NodeType
        A list of nodes. Nodes can be of any immutable type, e.g., integer, float, or string.
        We will usually use a list of integers 1, ..., n.
    graph: dict
        A dictionnary that contains the adjacency list of each node in the form
        graph[node] = [(neighbor1, p1, d1), (neighbor1, p1, d1), ...]
        where p1 is the minimal power on the edge (node, neighbor1) and d1 is the distance on the edge
    nb_nodes: int
        The number of nodes.
    nb_edges: int
        The number of edges. 
    """

    def __init__(self, nodes=[]):
        """
        Initializes the graph with a set of nodes, and no edges. 
        Parameters: 
        -----------
        nodes: list, optional
            A list of nodes. Default is empty.
        """
        self.nodes = nodes
        self.graph = dict([(n, []) for n in nodes])
        self.nb_nodes = len(nodes)
        self.nb_edges = 0
    

    def __str__(self):
        """Prints the graph as a list of neighbors for each node (one per line)"""
        if not self.graph:
            output = "The graph is empty"            
        else:
            output = f"The graph has {self.nb_nodes} nodes and {self.nb_edges} edges.\n"
            for source, destination in self.graph.items():
                output += f"{source}-->{destination}\n"
        return output
    
    def add_edge(self, node1, node2, power_min, dist=1):
        if node1 not in self.nodes: 
            self.nodes.append(node1) 
            self.graph[node1]=[] 
            self.nb_nodes+=1 
        if node2 not in self.nodes: 
            self.nodes.append(node2) 
            self.graph[node2]=[] 
            self.nb_nodes+=1 
        self.graph[node1].append((node2,power_min,dist)) 
        self.graph[node2].append((node1,power_min,dist)) 
        self.nb_edges+=1 
        return self.graph
    

    def get_path_with_power(self, src, dest, power):
            W=[]
            for l in self.connected_components(): #l est un element de la liste obtenu par la meth comp 
                if src in l:
                    W=l


            if dest in W: #cad si dep et arrivee dans la meme comp alors on peut les relier
                visite=[]
                chemin=[src] # si on def chemin dans explorer a chaque fois qu'on explore un voisin le chemin va changer et ne sera plus initialement debutant de src
                def explorer(ville):
                    if ville == dest:
                        return chemin #on n'a pas besoin de voir la puissance comme c'est la meme ville donc y a pas de route a traversee
                    visite.append(ville) # je l'avais mis a la fin de la boucle for mais ca ne marche pas vu que ca rajoute la ville visitee a la fin apres avoir reparcouru les voisins deja visites
                    for voisins in self.graph[ville]:
                        voisin=voisins[0]
                        puissance=voisins[1]
                        if voisin == dest:
                            if power >= puissance:
                                chemin.append(dest)
                                return chemin
                            else:
                                return None
                        else:
                            if voisin not in visite and power>=puissance:
                                chemin.append(voisin)
                                if explorer(voisin) is None:
                                    chemin.pop( ) #pour effacer toutes les villes ajouter inutilles
                                else:
                                    return chemin
                                    
                        
                return explorer(src)

    


    

    def connected_components(self):
        L=[]
        def explorer(i):
            U.append(i)
            for W in self.graph[i]:
                if W[0] not in U :
                    explorer(W[0])
        for i in self.graph:
            Signe=1
            for l in L :
                if i in l : 
                    Signe=-1
            if Signe==1:
                U=[]
                explorer(i)
                L.append(U)
        return L
        #ajouter alg pr complexite

    def connected_components_set(self):
        """
        The result should be a set of frozensets (one per component), 
        For instance, for network01.in: {frozenset({1, 2, 3}), frozenset({4, 5, 6, 7})}
        """
        return set(map(frozenset, self.connected_components()))
    
    def min_power(self, src, dest): 
        maxi=0
        for node in self.nodes: # on doit recherche la puiss max dans tous le graphe pas juste dans les voisins de src
            for voisins in self.graph[node]:
                if voisins[1]>maxi :
                    maxi=voisins[1]  #je ne vais pas faire ca pour min pour ne pas reparcourir if y a plus de chance de trouver la puissance en partant de 0 que de pqrtir de la puissance min
        
        puiss_min=0
        puiss_max=maxi
        chemin =[]
        
        # comme la recherche binaire consiste a divise en 2 partie a peu pres egale on va divise les seg de puiss de bornes puiss min et puiss max
        while puiss_min < puiss_max :               # si on met <=; en cas d'egalite on aura puiss=0 et apres puiss_min=0 et on pourrait rentrer dans des boucles infinis
            puiss = (puiss_max + puiss_min)//2      #avec le - ca marche pas car dans des cas on ne sera pas dans l'intervalle voulu
            if self.get_path_with_power(src, dest, puiss) is not None:
                puiss_max=puiss #on essaye de trouver une puiss plus petite que celle trouver
            else:
                puiss_min = puiss+1 # on recherche dans la partie contenant les valeurs supperieur a puiss comme la puissance "puiss" ne suffit pas pour le parcours, si on rajoute pas le 1 on aura un prob qd on trouve la puiss minimale la boucle while rstera infini
        
        chemin= self.get_path_with_power(src, dest, puiss_max) # la derniere fois ou on rentrera dans la boucle puiss va etre modifie eton rentrera dans le cas else donc on ne peut pas mettre puiss
        return (chemin, puiss_max)



def graph_from_file(filename):
    f = open("/home/onyxia/work/ensae-prog23/"+filename, "r") #On rajoute le début du chemin pour que le programme trouve le chemin du fichier 
    L = f.readlines()#On transforme le tableau en une liste de chaîne de caractères, avec une chaîne = une ligne 
    lignes=[] 
    g=Graph([]) 
    for i in range(1,len(L)): 
        lignes.append(L[i].split()) #"lignes" est une liste, donc les éléments (qui représentent les lignes de notre tableau) sont des listes de chaînes de caractères 
    for line in lignes: 
        if len(line)==3: #cad les lignes qui contiennent depart arrivee puissance
            g.add_edge(int(line[0]),int(line[1]),int(line[2]),1) 
        else : 
            g.add_edge(int(line[0]),int(line[1]),int(line[2]),int(line[3])) 
    #Attention ! Tous les sommets ne sont pas forcément reliés à d'autres sommets ! Dans cette partie du code, on s'occupe de mettre dans le graphe les sommets isolés 
    nb_nodes=int(L[0].split()[0]) #Le nombre de sommets est donné par le premier nombre de la première ligne 
    for n in range(1,nb_nodes+1): #On suppose ici que s'il y a n noeuds, tous les noeuds sont exactement tous les numéros de 1 à n. 
        if n not in g.graph: 
            g.graph[n]=[] 
            g.nb_nodes+=1 #Le nombre d'arêtes n'a pas été modifié, mais le nombre de sommets a lui changé 
    return g 

