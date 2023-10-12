from main import osmnx
from main import de_osmnx_a_diccionari
from main import imprimir_llista_adjacencia
from main import clicar_mapa_interactiu
from main import trobar_coordenada_mes_propera
from main import trobar_node_per_coordenades
from main import llista_tuples_coordenades
from main import uniform_cost_search
from main import imprimir_mapa_interactiu

# https://www.openstreetmap.org/#map=13/41.6880/2.3114

print("ROUTE FINDER")
print("Aquest programa et permet seleccionar dos punts d'un mapa del poble o de la ciutat que ")
print("vulguis i et traça el camí més curt entre aquests. Per començar, pensa en un poble o ")
print("una ciutat i escriu-lo a continuació:")
poble = input("·Nom del poble o de la ciutat:\n")
print("Ara, escriu el país on es situa el poble:")
pais = input("·Nom del país:\n")
print()

lloc = (str(poble) + "," + str(pais))
graf_omsnx = osmnx.graph_from_place(lloc, network_type='drive')

print("Informació bàsica del graf: \n", osmnx.basic_stats(graf_omsnx), "\n")

print("Aquí tens imprès per pantalla una imatge del graf generat a partir del teu poble triat. ")
print("Per continuar amb el programa, clica la creu per tancar la imatge.")

osmnx.plot_graph(graf_omsnx)
graf = de_osmnx_a_diccionari(graf_omsnx)

imprimir_llista_adjacencia(graf)

print("\nA continuació, si estàs preparat, escriu la paraula preparat i clica l'enter. A continuació, veuràs un mapa ")
print("del teu poble o de la teva ciutat triada. Quan hagis decidit quin punt serà l'inici de la teva ruta, fes clic")
print(" a sobre i introdueix aquí sota les coordenades que veuràs.")

f = input()
print("Som-hi!")
clicar_mapa_interactiu(graf_omsnx)

node_inici_lat = float(input("· Latitud:"))
node_inici_lon = float(input("· Longitud:"))
coordenada_inici = (node_inici_lat, node_inici_lon)
veritable_coordenada_inici = trobar_coordenada_mes_propera(coordenada_inici,
                                                           llista_tuples_coordenades(graf_omsnx))

print("\nAra, selecciona quin punt del mapa serà el destí de la teva ruta i clica a sobre. Un cop fet ")
print("això, veuràs les coordenades del punt. Introdueix-les a continuació:")
node_desti_lat = float(input("· Latitud:"))
node_desti_lon = float(input("· Longitud:"))
coordenada_desti = (node_desti_lat, node_desti_lon)
veritable_coordenada_desti = trobar_coordenada_mes_propera(coordenada_desti,
                                                           llista_tuples_coordenades(graf_omsnx))

node_inici = trobar_node_per_coordenades(graf_omsnx, veritable_coordenada_inici)
node_desti = trobar_node_per_coordenades(graf_omsnx, veritable_coordenada_desti)

resultat = uniform_cost_search(node_inici, node_desti, graf)
cami_nodes, longitud = resultat
print(f"\nEl camí més curt entre els dos punts seleccionats passa pels següents nodes: " + str(
    cami_nodes) + "\nLa distància recorreguda és: " + str(longitud) + "m.")

imprimir_mapa_interactiu(graf_omsnx, node_inici, node_desti, cami_nodes)
