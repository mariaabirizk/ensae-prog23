from graph import Graph, graph_from_file

'''
g = Graph([]) # creation dun objet de type Graph
g.add_edge("Paris", "Palaiseau", 4, 20)
print(g) # affichage du graphe
'''

data_path = "input/"

fichier_trucks = "trucks.1.in"
fichier_routes = "routes.1.in"
fichier_network = "network.1.in"
#f=function_profit(fichier_trucks,fichier_routes,fichier_network)
#print(f)

g = graph_from_file(data_path + fichier_network)
print(g)
l=liste_from_file(data_path + fichier_routes)
print(l)
la=liste_from_file(data_path + fichier_trucks)
print(la)

