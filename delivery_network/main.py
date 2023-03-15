from graph import Graph, graph_from_file

'''
g = Graph([]) # creation dun objet de type Graph
g.add_edge("Paris", "Palaiseau", 4, 20)
print(g) # affichage du graphe
'''

data_path = "input/"
file_name = "network.04.in"

g = graph_from_file(data_path + file_name)
print(g.get_path_with_power(1,3,100))



