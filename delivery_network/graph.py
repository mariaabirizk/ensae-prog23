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
        """
        Adds an edge to the graph. Graphs are not oriented, hence an edge is added to the adjacency list of both end nodes. 

        Parameters: 
        -----------
        node1: NodeType
            First end (node) of the edge
        node2: NodeType
            Second end (node) of the edge
        power_min: numeric (int or float)
            Minimum power on this edge
        dist: numeric (int or float), optional
            Distance between node1 and node2 on the edge. Default is 1.
        """
        raise NotImplementedError
    

    def get_path_with_power(self, src, dest, power):
        W=[]
        for l in self.connect_components_set() :
            if src in l:
                W=l
        if dest in W : #cad si dep et arrivee dans la meme comp alors on peut les relier
            
                def explorer(src):
                    for j in range(0,self.graph[src]): # j est couple du vois et puiss et dist
                        #j(0) sera tjrs ds self.nodes car c est le voisin de src
                        if j== dest:
                            print("lbbllb")
                        else:
                            a=self.graph[j]
                            voisinsj=a.remove((src,power_min,dist)) #rev powermin et dist #ca me donne les vois de j sans src

                            if voisinsj == []: #cad si j n a pas de voisin
                                if j == dest:
                                    print("le chemin est"+(src,j,dest)) #modifier le print

                            #cad cas else j n'a pas de vois et n est pas la dest on passe a un autre j, ca sort de if
                            else: #cas ou j a des voisins
                                explorer(j) #PROB! on peut mettre deux entrees a la ftc expplorer la 2e est une liste 




                    parent=j
                    U.append(j)
                    for W in self.graph[j]:
                        if W[0] not in U :
                            if W[0]= dest:
                                errêter
                            elif W[0]=[]
                                explorer(W[0])
            for i in self.graph[i]:
            Signe=1
            for l in L :
                if i in l : 
                    Signe=-1
            if Signe==1:
                U=[]
                explorer(i)
                L.append(U)   
        else :
            return None

            
     
    

    def connected_components(self):
        raise NotImplementedError


    def connected_components_set(self):
        """
        The result should be a set of frozensets (one per component), 
        For instance, for network01.in: {frozenset({1, 2, 3}), frozenset({4, 5, 6, 7})}
        """
        return set(map(frozenset, self.connected_components()))
    
    def min_power(self, src, dest):
        """
        Should return path, min_power. 
        """
        raise NotImplementedError


def graph_from_file(filename):
    """
    Reads a text file and returns the graph as an object of the Graph class.

    The file should have the following format: 
        The first line of the file is 'n m'
        The next m lines have 'node1 node2 power_min dist' or 'node1 node2 power_min' (if dist is missing, it will be set to 1 by default)
        The nodes (node1, node2) should be named 1..n
        All values are integers.

    Parameters: 
    -----------
    filename: str
        The name of the file

    Outputs: 
    -----------
    G: Graph
        An object of the class Graph with the graph from file_name.
    """
    raise NotImplementedError