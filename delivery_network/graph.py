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

    '''
    def function_question18_methode1(fichier_trucks,fichier_routes,fichier_network):
       
        lr=liste_from_file("input/"+fichier_routes)
        g= graph_from_file("input/"+fichier_network)
        #pour le fichier trucks
        lt=liste_from_file("input/"+fichier_trucks) # [(p1,c1) , (p2,c2), ........]
        lt.sort(key=lambda x: x[1])


        b= 25*(10**9) #contrainte budg
        
        #meth1 , exacte
        for j in range (0,len(lr)):
            def fct(j,b):
                depenses=0
                umax= 0
                u=0
                c=0
                resultat=[]
                resultat_final=[]
                l=[]
                
                for i in range (j,len(lr)): #on somme les utilites en partant de la ligne i et jusqu'a la ligne k ou on aura depasse la cb
                    while depenses<=b:
                        u=u+lr[i][1]
                        pmin=g.min_power(lr[i][0])
                        a=False
                        while a==False:
                            for j in range (0,len(lt)):
                                if lt[j][0]>= pmin:
                                    puiss=lt[j][0]
                                    c= lt[j][1] 
                                    a=True
                                    break #revoir l'ecriture, j'ai ajoute break parceque je pense qu'il va faire toutes les iterations dans lt sinon    
                        depenses=depenses+c
                        resultat.append((puiss,c),lr[i][0])
                        derniere_ligne_atteinte=i

                    l.append((u,derniere_ligne_atteinte,resultat)) # je cree une liste l dont les element sont les utilites finales et les trajet associees aux camions, apres je prendrai max u de la liste l
                return l
            

            

            for i in range (0,len(lr)):
                l=fct(i,b)
                for k in range ((i+1),len(lr)): #en partant de ma ligne j je veux sommer mais en enlevant une ligne entre j+1 et la fin
                    #u_en_partant_de_la_lignei on a atteint utilite=l[i][0]
                    u= l[i][0] - lr[k][1]        #u-u(lignek), maintenant en partant de cette utilite on voit si on peut augmenter notre utilite encore
                    #maintenant en partant de u=la somme donnee ci dessus on doit continuer a sommer avec u des lignes non deja visites
                    m= l[i][1] +1   #on commence a sommer les utilites a partir de la ligne (derniere_ligne_atteinte +1)
                    for v in range (m,len(lr)):
                        #on reprend algo on comme avec cb .....
                        #et on rajoute les utilites atteintes et les camions associees au trajet dans ces cas a la liste l

        l.sort()
        return (umax,resultat_final)=l[len(l)]
'''







def function_profit(fichier_trucks,fichier_routes,fichier_network): #methode2 rapide
    # je veux acceder aux lignes du fichier_routes, chaque ligne i>=1 represente le trajet i=(ville1,ville2) et son utilite i 
    lr=liste_from_file("input/"+ fichier_routes)        
    lr.sort(key=lambda x: x[1]) #lr sera triee par ordre croissant d'utilite 
            
    g= graph_from_file("input/"+fichier_network)

    #pour le fichier trucks
    lt=liste_from_file("input/"+fichier_trucks) # [(p1,c1) , (p2,c2), ........]
    lt.sort(key=lambda x: x[1])

    b= 25*(10**9) #contrainte budg
    depenses=0
    umax= 0
    c=0
    resultat=[]
    
    for i in range (0,len(lr)): 
        l=len(lr)
        if depenses <= b:
            umax=umax+lr[l-1-i][1]   #l-i car on veux sommer les utilites en partant des plus grandes utilites 
            p=g.min_power(lr[l-1-i][0][0],lr[l-1-i][0][1]) #min_power sur le trajet associe a l'utilite prise 
            pmin=p[1]
            a=False
            while a==False:
                for j in range (0,len(lt)):
                    if lt[j][0]>= pmin:
                        puiss=lt[j][0]
                        c= lt[j][1] 
                        a=True                            
                        resultat.append(((puiss,c),lr[l-1-i][0])) #revoir si qd ils disent return le camion et affection sur le trajet ils veulent (p,c) du camion et pas numero de la ligne associee a ce couple
                        depenses=depenses+c
                        break #j'ai ajoute break parceque je pense qu'il va faire toutes les iterations dans lt sinon

    return (umax,resultat)

def liste_from_file(filename):
    f = open("/home/onyxia/work/ensae-prog23/"+filename, "r") 
    L = f.readlines()
    lignes=[] 
    liste=[]
    for i in range(1,len(L)): 
        lignes.append(L[i].split())  
    for line in lignes: 
        if len(line)==2: #je l'utilise pour le fichier trucks
            liste.append((int(line[0]) ,int(line[1]))) # (p,c)
        if len(line)==3: #je l'utilise pour le fichier routes
            liste.append(((int(line[0]),int(line[1])),int(line[2]))) #pour les fichiers trucks on aura ((villea,villeb), uab)
    return liste



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

#Pour le Compte Rendu, cette fonction kruskal n'est pas notre version finale, on n'a pas encore obtenu nos resultats attendus
def kruskal(graphe): #trions la liste des aretes
    #1-doit retourner un element de type Graph de meme nombre de noeuds que graphe
    nouvgraphe=Graph()

    #2- trions les aretes de "graphe" par ordre croissant

    d={} # je veux stocker dans d les aretes et la puissance associee a chacune
    l=[] #je veux stocker dans l les puissances
    for i in range (0,len(graphe.graph)): # ma bhot () car c est pas une methode mais attribut
        for voisin in graphe.graph[i]: #cad je regarde pour le noeud i ses voisins
            if (i,voisin[0]) or (voisin[0],i) not in d:
                d[voisin[1]].append(i,voisin[0])
                l.append(voisin[1])
    #on obtient ainsi d un dictionnaire dont les cles sont les puissances des aretes et les valeurs sont les aretes
    l.sort()
    #a present pour acceder aux aretes de puissance dans l: on a qu'a faire d[la puissance en question]

    #3-construisons nouvgraphe
    for j in range (0,len(l)): #pour une puissance j 
        for arete in d[l[j]]: #d[l[j]] peut contenir plusieurs aretes 

            #dans if on met une condition pour ne pas former de cycle en ajoutant cette nouvelle arete
            # si les deux etremites des aretes ont etes visites plus que 2 fois on risque d'obtenir un cycle si on la rajoute une 3e
            if nouvgraphe.get_path_with_power(arete[0], arete[1], l[-1]) is not None:
                nouvgraphe.add_edge(arete[0],arete[1],l[j])
############################################ continuer et mettre la fonction dans la class Graph 
    return (nouvgraphe)
