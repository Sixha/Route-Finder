from main import de_diccionari_a_networkx
from main import imprimir_imatge_graf_simple
from main import imprimir_llista_adjacencia
from main import uniform_cost_search

graf = {
    'A': {'B': 5, 'C': 2},
    'B': {'A': 5, 'C': 4, 'D': 9, 'E': 7},
    'C': {'A': 2, 'B': 4, 'F': 3},
    'D': {'B': 9, 'E': 8, 'G': 2},
    'E': {'B': 7, 'D': 8, 'F': 6},
    'F': {'C': 3, 'E': 6, 'H': 5},
    'G': {'D': 2, 'H': 1},
    'H': {'F': 5, 'G': 1},
    'N': {}
}
print("ROUTE FINDER")
print("Aquest programa et permet seleccionar dos nodes del graf introduit anteriorment")
print("i et traça el camí més curt entre aquests.\n")
graf_networkx = de_diccionari_a_networkx(graf)
print(f"El teu graf té els següents nodes: " + str(
    graf_networkx.nodes()) + "\nEl teu graf té les següents arestes: " + str(graf_networkx.edges()) + "\n")

print("A continuació, pots veure una possible representació gràfica del teu graf. Quan vulguis ")
print("seguir endavant amb el programa, tenca la imatge amb la creu.")
imprimir_imatge_graf_simple(graf_networkx)

imprimir_llista_adjacencia(graf)
print()
node_inici = input("Introdueix el node inici:\n")
node_desti = input("Introdueix el node desti:\n")
resultat = uniform_cost_search(node_inici, node_desti, graf)
cami, longitud = resultat
print(f"\nEl camí més curt entre els nodes triats és: " + str(cami) + "\nLa distància recorreguda són " + str(
    longitud) + " unitats.")

